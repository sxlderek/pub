# WhatsApp Bridge Troubleshooting

## Common Issues and Solutions

### Issue: "Cannot connect to host localhost:3000"

**Symptoms:**
- `send_message(action='list')` shows WhatsApp as available
- Sending messages fails with connection error to localhost:3000
- WhatsApp gateway service not responding

**Root Cause:**
The WhatsApp bridge service (`bridge.js`) is not running or failed to start.

**Diagnosis Steps:**

1. Check if service is running:
```bash
ps aux | grep bridge.js
```

2. Check if port 3000 is in use:
```bash
netstat -tlnp | grep :3000
# or
curl http://localhost:3000/health
```

Expected healthy response:
```json
{"status":"connected","queueLength":0,"uptime":52.280498368}
```

**Solution:**

1. Navigate to bridge directory and install dependencies:
```bash
cd /opt/hermes/scripts/whatsapp-bridge
npm install --cache /tmp/npm-cache
```

2. If npm fails with EACCES (permission denied on /opt/data/home/.npm):
   - Use alternate cache: `npm install --cache /tmp/npm-cache`
   - This bypasses root-owned cache files

3. If npm fails with ENOTEMPTY (directory not empty):
   - Clean and reinstall: `rm -rf node_modules && npm install --cache /tmp/npm-cache`

4. Start the bridge:
```bash
node bridge.js
# or in background
node bridge.js &
```

5. Verify it's running:
```bash
curl http://localhost:3000/health
```

### Issue: Port 3000 Already in Use

**Symptoms:**
- Starting bridge.js fails with "EADDRINUSE: address already in use 127.0.0.1:3000"

**Root Cause:**
Bridge is already running (possibly from previous session or auto-start).

**Solution:**
1. Verify service is running and healthy:
```bash
curl http://localhost:3000/health
```

2. If healthy, no action needed - service is already operational

3. If unhealthy or unresponsive, kill and restart:
```bash
pkill -f bridge.js
cd /opt/hermes/scripts/whatsapp-bridge && node bridge.js &
```

### Issue: npm Permission Errors

**Symptoms:**
- npm install fails with EACCES
- Error mentions root-owned files in /opt/data/home/.npm

**Root Cause:**
npm cache contains root-owned files from previous runs.

**Solution:**
Use alternate cache location:
```bash
npm install --cache /tmp/npm-cache
```

Do NOT attempt to chown the cache - user hermes (uid 10000) cannot change ownership of root files even though it can run apt-get.

## Bridge Service Details

**Location:** `/opt/hermes/scripts/whatsapp-bridge/`
**Main file:** `bridge.js` (not index.js)
**Port:** 3000 (localhost only)
**Health endpoint:** `http://localhost:3000/health`
**Session path:** `/opt/data/whatsapp/session` (configured in Hermes config.yaml)

## Integration with Selfcheck

The selfcheck script should:
1. Check if bridge is running via health endpoint
2. If not running, attempt to start it
3. Report status in final summary
4. Flag if manual intervention needed (e.g., QR code scan required)

## Session Notes

- 2026-05-02: Discovered bridge was already running after restart, causing EADDRINUSE error
- npm cache workaround (`--cache /tmp/npm-cache`) successfully bypasses permission issues
- Health check endpoint returns JSON with status, queueLength, and uptime
