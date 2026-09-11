#!/bin/bash
# Sandbox entrypoint for banking API simulation

set -e

# Initialize sandbox environment
mkdir -p /logs/agent /logs/verifier /logs/sandbox
echo "Starting banking sandbox..."
export SANDBOX_MODE=true
export API_BASE="https://api.maybank2u.com/v2"

# Log startup
echo "[$(date -Iseconds)] Sandbox initialized" > /logs/sandbox.log

# Execute main command
exec "$@"
