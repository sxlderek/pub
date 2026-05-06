     1|---
     2|name: selfcheck-skill
     3|description: System health check for messaging channels and required tools
     4|version: 1.0.3
     5|tags: [system, health-check, diagnostics, messaging]
     6|author: Kiro
     7|created: 2026-05-02
     8|---
     9|
    10|# Selfcheck Skill
    11|
    12|Comprehensive system health check to verify messaging channels and required tools are working properly.
    13|
    14|## When to Use
    15|
    16|- On startup or after configuration changes
    17|- When messaging or media processing issues are suspected
    18|- Before critical operations that depend on messaging or media tools
    19|- Periodically as a maintenance check
    20|- Recommended schedule: run twice daily at **09:00** and **21:00 HKT**
    21|
    22|## What This Checks
    23|
    24|1. **Messaging Channels**
    25|   - WhatsApp connectivity and configuration
    26|   - Telegram connectivity and configuration
    27|   - Any other configured chat channels in the future
    28|
    29|2. **Required Tools**
    30|   - curl
    31|   - ffmpeg
    32|   - ImageMagick (`magick` / `convert`)
    33|   - ping
    34|   - nslookup
    35|   - whois
    36|   - nmap
    37|   - pandoc
    38|
    39|3. **Auto-Repair**
    40|   - Attempts to install missing packages
    41|   - Fixes common configuration issues
    42|   - Reports what was fixed and what needs manual intervention
    43|
    44|## Procedure
    45|
    46|### 1. Run the selfcheck script
    47|
    48|The script checks tools and WhatsApp bridge health:
    49|
    50|```bash
    51|python3 /opt/data/skills/selfcheck-skill/scripts/selfcheck.py
    52|```
    53|
    54|This will:
    55|- Check the required tools with `command -v`
    56|- Check ffmpeg and ImageMagick version checks
    57|- Check WhatsApp bridge process and health endpoint
    58|- Auto-start WhatsApp bridge if not running (npm install + node bridge.js)
    59|
    60|### 2. Test Messaging Channels (Agent-level)
    61|
    62|After the script completes, the agent MUST test actual message sending:
    63|
    64|```python
    65|# Test WhatsApp
    66|try:
    67|    send_message(target='whatsapp', message='✅ Selfcheck: WhatsApp operational')
    68|    whatsapp_status = '✅ Working'
    69|except Exception as e:
    70|    whatsapp_status = f'❌ Failed: {e}'
    71|    # If failed, try to repair WhatsApp bridge:
    72|    # cd /opt/hermes/scripts/whatsapp-bridge
    73|    # rm -rf node_modules
    74|    # npm install --cache /tmp/npm-cache
    75|    # node bridge.js (background)
    76|
    77|# Test Telegram  
    78|try:
    79|    send_message(target='telegram', message='✅ Selfcheck: Telegram operational')
    80|    telegram_status = '✅ Working'
    81|except Exception as e:
    82|    telegram_status = f'❌ Failed: {e}'
    83|    # If Telegram fails, check Telegram bot token in config
    84|```
    85|
    86|**Expected output:**
    87|- Messages successfully delivered to both platforms
    88|- No connection errors
    89|
    90|**If WhatsApp fails after bridge repair:**
    91|- Check `/opt/hermes/scripts/whatsapp-bridge` exists
    92|- Verify port 3000 is not blocked
    93|- Check bridge logs for authentication issues
    94|
    95|**If Telegram fails:**
    96|- Verify Telegram bot token in `/opt/data/config.yaml`
    97|- Check network connectivity
    98|- Review Hermes gateway logs
    99|
   100|**Note:** The selfcheck script can only report that these tests are required; the actual `send_message` calls must be made by the Hermes agent wrapper that runs the script.
   101|
   102|### 3. Generate Final Report
   103|
   104|Combine script output and messaging test results into a comprehensive report:
   105|
   106|```
   107|✅ SELFCHECK COMPLETE
   108|
   109|TOOLS:
   110|  curl: ✅ Present
   111|  ffmpeg: ✅ Working
   112|  imagemagick: ✅ Working
   113|  ping: ✅ Present
   114|  nslookup: ✅ Present
   115|  whois: ✅ Present
   116|  nmap: ✅ Present
   117|  pandoc: ✅ Present
   118|
   119|MESSAGING:
   120|  whatsapp_bridge: ✅ Running (health: {"status":"connected"})
   121|  whatsapp: ✅ Message delivered
   122|  telegram: ✅ Message delivered
   123|
   124|🔧 AUTO-FIXED:
   125|  - Started WhatsApp bridge
   126|
   127|All systems operational.
   128|```
   129|
   130|## Example Implementation
   131|
   132|```python
   133|#!/usr/bin/env python3
   134|import subprocess
   135|import sys
   136|
   137|results = {
   138|    'messaging': {},
   139|    'tools': {},
   140|    'fixes': []
   141|}
   142|
   143|# Check messaging channels
   144|print("🔍 Checking messaging channels...")
   145|# Use send_message tool to list channels
   146|# Parse output and check for WhatsApp and Telegram
   147|
   148|# Check ffmpeg
   149|print("🔍 Checking ffmpeg...")
   150|try:
   151|    result = subprocess.run(['ffmpeg', '-version'], 
   152|                          capture_output=True, text=True, timeout=5)
   153|    if result.returncode == 0:
   154|        results['tools']['ffmpeg'] = '✅ Working'
   155|    else:
   156|        raise Exception("ffmpeg check failed")
   157|except:
   158|    print("🔧 Installing ffmpeg...")
   159|    subprocess.run(['apt-get', 'update'], check=True)
   160|    subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'], check=True)
   161|    results['fixes'].append('Installed ffmpeg')
   162|    results['tools']['ffmpeg'] = '✅ Fixed'
   163|
   164|# Check ImageMagick
   165|print("🔍 Checking ImageMagick...")
   166|try:
   167|    result = subprocess.run(['magick', '-version'], 
   168|                          capture_output=True, text=True, timeout=5)
   169|    if result.returncode == 0:
   170|        results['tools']['imagemagick'] = '✅ Working'
   171|    else:
   172|        raise Exception("ImageMagick check failed")
   173|except:
   174|    try:
   175|        result = subprocess.run(['convert', '-version'], 
   176|                              capture_output=True, text=True, timeout=5)
   177|        if result.returncode == 0:
   178|            results['tools']['imagemagick'] = '✅ Working (legacy)'
   179|        else:
   180|            raise Exception("ImageMagick check failed")
   181|    except:
   182|        print("🔧 Installing ImageMagick...")
   183|        subprocess.run(['apt-get', 'update'], check=True)
   184|        subprocess.run(['apt-get', 'install', '-y', 'imagemagick'], check=True)
   185|        results['fixes'].append('Installed ImageMagick')
   186|        results['tools']['imagemagick'] = '✅ Fixed'
   187|
   188|# Print report
   189|print("\n" + "="*50)
   190|print("SELFCHECK REPORT")
   191|print("="*50)
   192|for category, items in results.items():
   193|    if category != 'fixes':
   194|        print(f"\n{category.upper()}:")
   195|        for name, status in items.items():
   196|            print(f"  {name}: {status}")
   197|
   198|if results['fixes']:
   199|    print(f"\n🔧 AUTO-FIXED:")
   200|    for fix in results['fixes']:
   201|        print(f"  - {fix}")
   202|```
   203|
   204|## Pitfalls
   205|
   206|- The script requires actual Hermes `send_message` access in the wrapper layer to verify WhatsApp and Telegram delivery
   207|- Required tool checks should use `command -v` first; only then try install/repair actions for missing items
   208|- ffmpeg and ImageMagick must be installed for tool checks to pass
   209|- In Docker environments, use `python3` explicitly (not `python`) - the script has a proper shebang but manual invocation needs `python3 /path/to/script.py`
   210|- WhatsApp gateway requires a separate service (`hermes-whatsapp`) running on port 3000 - if `send_message(action='list')` shows WhatsApp but sending fails with "Cannot connect to host localhost:3000", the gateway service is down
   211|  - **Fix procedure**: `cd /opt/hermes/scripts/whatsapp-bridge && npm install --cache /tmp/npm-cache && node bridge.js` (run in background)
   212|  - Check if already running: `ps aux | grep bridge.js` or `curl http://localhost:3000/health` (should return `{"status":"connected"}`)
   213|  - If port 3000 already in use, the service is likely already running - verify with health check before attempting restart
   214|  - In this environment, user `hermes` (uid 10000) can run apt-get
   215|
   216|2. **Ephemeral State**
   217|   - Container state is ephemeral
   218|   - Installed packages won't persist across container rebuilds
   219|   - Consider adding to Dockerfile for permanent fixes
   220|
   221|3. **Network Issues**
   222|   - Gateway services may be down temporarily
   223|   - Check network connectivity before assuming configuration issues
   224|
   225|4. **Version Compatibility**
   226|   - ImageMagick 6.x uses `convert` command
   227|   - ImageMagick 7.x uses `magick` command
   228|   - Check both for compatibility
   229|
   230|5. **Silent Failures**
   231|   - Some tools may be installed but misconfigured
   232|   - Test actual functionality, not just presence
   233|
   234|## Success Criteria
   235|
   236|- All messaging channels show "Connected ✓"
   237|- ffmpeg and ImageMagick respond to version checks
   238|- Test messages successfully delivered (if testing enabled)
   239|- No manual intervention required
   240|
   241|## Related Skills
   242|
   243|- `hermes-agent` - For Hermes configuration and troubleshooting
   244|- `telegram-gateway-setup` - For Telegram-specific configuration
   245|
   246|## Support Files
   247|
   248|- `references/live-selfcheck-verification.md` - Live verification notes for tool inventory and actual WhatsApp/Telegram delivery tests
   249|
   250|## Session Notes
   251|
   252|### 2026-05-02: WhatsApp Bridge Auto-Repair Success
   253|- User reported WhatsApp channel non-functioning after restart
   254|- Script successfully detected bridge was down and auto-repaired it
   255|- npm install with `--cache /tmp/npm-cache` avoided permission issues
   256|- Bridge started successfully and health check passed
   257|- Actual message delivery tests to both WhatsApp and Telegram confirmed end-to-end functionality
   258|- User feedback: "welcome back. you survived from self restart. However, my whatsapp channel is still non-functioning." → Fixed with auto-repair
   259|- Skill published to GitHub at https://github.com/sxlderek/pub/tree/main/skills/selfcheck-skill
   260|
   261|## Reference Files
   262|
   263|- `references/whatsapp-bridge-troubleshooting.md` - Comprehensive WhatsApp bridge troubleshooting: startup procedures, npm cache permission fixes, health check patterns, session mismatch debugging, and the critical lesson that actual message sending is required for verification (not just process/health checks)
   264|
   265|## Notes
   266|
   267|- This skill should be run in a safe, non-production context first
   268|- Auto-installation requires appropriate permissions
   269|- Some fixes may require container restart to take effect
   270|- Keep this skill updated as new channels or tools are added
   271|