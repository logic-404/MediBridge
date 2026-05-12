#!/bin/sh
set -e

DB_PATH="${MEDIBRIDGE_DATA_DIR:-${MEDIBRIDGE_ROOT:-/app}/data}/medibridge.db"

if [ ! -f "$DB_PATH" ] && [ -d "${MEDIBRIDGE_ROOT:-/app}/knowledge" ]; then
    echo "Database not found — running ingest..."
    python -m medibridge.data.ingest
fi

exec "$@"
