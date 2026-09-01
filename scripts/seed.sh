# Local development and seed helper
# Usage: ./scripts/seed.sh

set -euo pipefail

# Creates a minimal seeded project via the API (assumes backend is running at localhost:8000)
API=${API_URL:-http://localhost:8000}
TOKEN=${DEV_TOKEN:-}

if [ -z "$TOKEN" ]; then
  echo "No DEV_TOKEN provided; attempting anonymous create if allowed. To set: export DEV_TOKEN=..."
fi

echo "Creating sample project via API: $API"

curl -s -X POST "$API/projects" \
  ${TOKEN:+-H "Authorization: Bearer $TOKEN"} \
  -H "Content-Type: application/json" \
  -d '{"project_name":"Seed Project","description":"Seeded project for local dev"}' | jq .

echo "Seed complete. Check http://localhost:3000/projects/1 (IDs may differ based on DB state)."
