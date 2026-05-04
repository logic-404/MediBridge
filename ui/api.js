// MediBridge frontend ↔ FastAPI client.
// Same-origin fetch (frontend is mounted by uvicorn at /). All paths relative.

(function () {
  async function _request(method, path, body) {
    const res = await fetch(path, {
      method,
      headers: body !== undefined ? { 'Content-Type': 'application/json' } : undefined,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    if (res.status === 204) return null;
    if (!res.ok) {
      let detail = '';
      try { detail = (await res.json()).detail || ''; } catch {}
      const err = new Error(`HTTP ${res.status} ${res.statusText}${detail ? ' — ' + detail : ''}`);
      err.status = res.status;
      throw err;
    }
    return res.json();
  }

  function qs(params) {
    const usp = new URLSearchParams();
    Object.entries(params || {}).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') usp.set(k, v);
    });
    const s = usp.toString();
    return s ? '?' + s : '';
  }

  // SSE over POST: parse `event:` / `data:` framed lines from a streaming response body.
  async function chatStream({ message, history }, callbacks) {
    const { onToolCall, onToolResult, onMessage, onDone, onError } = callbacks || {};
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
      body: JSON.stringify({ message, history: history || [] }),
    });
    if (!res.ok || !res.body) {
      const err = new Error(`Chat HTTP ${res.status}`);
      onError && onError(err);
      throw err;
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = '';
    let curEvent = 'message';
    let curData = '';

    const flush = () => {
      if (!curData) { curEvent = 'message'; return; }
      let parsed;
      try { parsed = JSON.parse(curData); } catch { parsed = { raw: curData }; }
      if (curEvent === 'tool_call') onToolCall && onToolCall(parsed);
      else if (curEvent === 'tool_result') onToolResult && onToolResult(parsed);
      else if (curEvent === 'assistant_message') onMessage && onMessage(parsed);
      else if (curEvent === 'done') onDone && onDone();
      else if (curEvent === 'error') onError && onError(new Error(parsed.message || 'Stream error'));
      curEvent = 'message';
      curData = '';
    };

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let idx;
      while ((idx = buf.indexOf('\n')) >= 0) {
        const line = buf.slice(0, idx).replace(/\r$/, '');
        buf = buf.slice(idx + 1);
        if (line === '') { flush(); continue; }
        if (line.startsWith(':')) continue; // comment
        const colon = line.indexOf(':');
        const field = colon === -1 ? line : line.slice(0, colon);
        const value = colon === -1 ? '' : line.slice(colon + 1).replace(/^ /, '');
        if (field === 'event') curEvent = value;
        else if (field === 'data') curData += (curData ? '\n' : '') + value;
      }
    }
    flush();
  }

  window.api = {
    getInsurers: () => _request('GET', '/api/insurers'),
    getProfile: async () => {
      try { return await _request('GET', '/api/profile'); }
      catch (e) { if (e.status === 404) return null; throw e; }
    },
    saveProfile: (payload) => _request('PUT', '/api/profile', payload),
    deleteProfile: () => _request('DELETE', '/api/profile'),
    coverage: (item_num, setting) => _request('POST', '/api/coverage', { item_num, setting }),
    searchMbs: (q, limit = 8) => _request('GET', '/api/mbs/search' + qs({ q, limit })),
    getMbs: (item_num) => _request('GET', '/api/mbs/' + encodeURIComponent(item_num)),
    searchClinics: ({ postcode, suburb, type, billing } = {}) =>
      _request('GET', '/api/clinics' + qs({ postcode, suburb, type, billing })),
    clinicTypes: () => _request('GET', '/api/clinics/types'),
    clinicBilling: () => _request('GET', '/api/clinics/billing'),
    chatStream,
  };
})();
