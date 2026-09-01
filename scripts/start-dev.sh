#!/usr/bin/env bash
set -euo pipefail

# Start local dev stack (requires Docker & docker-compose)
# Usage: ./scripts/start-dev.sh

DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$DIR"

echo "Starting local dev stack with docker-compose..."

docker compose up --build -d

echo "Services started. Backend: http://localhost:8000, Frontend: http://localhost:3000"

echo "To view logs: docker compose logs -f backend"

