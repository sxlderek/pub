     1|# WhatsApp Bridge Troubleshooting
     2|
     3|## Common Issues and Fixes
     4|
     5|### Bridge Not Running
     6|
     7|**Symptoms:**
     8|- `send_message(target='whatsapp')` fails with "Cannot connect to host localhost:3000"
     9|- `curl http://localhost:3000/health` returns connection refused
    10|- `ps aux | grep bridge.js` shows no process
    11|
    12|**Root Cause:**
    13|The WhatsApp bridge is a separate Node.js service that must be running for WhatsApp messaging to work.
    14|
    15|**Fix:**
    16|```bash
    17|cd /opt/hermes/scripts/whatsapp-bridge
    18|rm -rf node_modules
    19|npm install --cache /tmp/npm-cache
    20|node bridge.js &  # Run in background
    21|```
    22|
    23|**Verification:**
    24|```bash
    25|# Check process
    26|ps aux | grep bridge.js | grep -v grep
    27|
    28|# Check health endpoint
    29|curl http://localhost:3000/health
    30|# Expected: {"status":"connected","queueLength":0,"uptime":...}
    31|```
    32|
    33|### Port 3000 Already in Use
    34|
    35|**Symptoms:**
    36|- Starting bridge.js fails with "EADDRINUSE: address already in use 127.0.0.1:3000"
    37|
    38|**Root Cause:**
    39|Bridge is already running (possibly from a previous startup).
    40|
    41|**Fix:**
    42|Don't start another instance. Verify the existing one is healthy:
    43|```bash
    44|curl http://localhost:3000/health
    45|```
    46|
    47|If unhealthy, kill and restart:
    48|```bash
    49|pkill -f bridge.js
    50|cd /opt/hermes/scripts/whatsapp-bridge
    51|node bridge.js &
    52|```
    53|
    54|### npm Cache Permission Issues
    55|
    56|**Symptoms:**
    57|- `npm install` fails with "EACCES" errors
    58|- Error mentions root-owned files in `~/.npm/_cacache`
    59|
    60|**Root Cause:**
    61|npm cache directory has root-owned files from a previous run.
    62|
    63|**Fix:**
    64|Use a temporary cache directory:
    65|```bash
    66|npm install --cache /tmp/npm-cache
    67|```
    68|
    69|**Why this works:**
    70|- `/tmp/npm-cache` is created fresh with correct permissions
    71|- Bypasses the corrupted `~/.npm` cache
    72|- Safe for ephemeral containers
    73|
    74|### Bridge Running But Messages Fail
    75|
    76|**Symptoms:**
    77|- Health endpoint returns `{"status":"connected"}`
    78|- Process is running
    79|- But `send_message(target='whatsapp')` still fails
    80|
    81|**Possible Causes:**
    82|1. **Session mismatch**: Bridge session path doesn't match Hermes config
    83|2. **Authentication expired**: WhatsApp session needs re-authentication
    84|3. **Network issue**: Bridge can't reach WhatsApp servers
    85|
    86|**Debug Steps:**
    87|```bash
    88|# Check bridge logs (if logging to file)
    89|tail -f /opt/hermes/scripts/whatsapp-bridge/logs/*.log
    90|
    91|# Check bridge command-line args
    92|ps aux | grep bridge.js
    93|
    94|# Verify session path matches config
    95|grep "session_path:" /opt/data/config.yaml
    96|```
    97|
    98|## Session Notes (2026-05-02)
    99|
   100|### User Correction
   101|When I initially said "I can't start it from inside this container since it's a host-level service", the user corrected me with the exact fix:
   102|```bash
   103|cd /opt/hermes/scripts/whatsapp-bridge
   104|npm install
   105|```
   106|
   107|This works because:
   108|- The bridge directory is accessible inside the container at `/opt/hermes/scripts/whatsapp-bridge`
   109|- The container has Node.js and npm installed
   110|- The container user (hermes, uid 10000) has write access to that directory
   111|- The bridge is meant to run inside the same container as the agent, not on the host
   112|
   113|**Lesson**: Don't assume services are "host-level" without checking. If the directory exists and is writable, try to fix it in-place.
   114|
   115|### Auto-Repair Pattern
   116|The selfcheck script now implements this pattern:
   117|1. Check if bridge process is running (`pgrep -f bridge.js`)
   118|2. Check health endpoint (`curl localhost:3000/health`)
   119|3. If either fails, auto-repair:
   120|   - Clean node_modules
   121|   - npm install with temp cache
   122|   - Start bridge in background
   123|4. Wait 3 seconds and verify health
   124|
   125|This pattern successfully fixed the bridge during testing.
   126|
   127|### Testing Requirements
   128|User emphasized: "you must send a message to whatsapp make sure it works"
   129|
   130|Not sufficient:
   131|- ❌ Checking if bridge process exists
   132|- ❌ Checking health endpoint only
   133|- ❌ Listing available channels with `send_message(action='list')`
   134|
   135|Required:
   136|- ✅ Actually send a test message with `send_message(target='whatsapp', message='...')`
   137|- ✅ Verify message delivery (check for success response)
   138|- ✅ Do the same for Telegram
   139|
   140|This ensures end-to-end functionality, not just component health.
   141|