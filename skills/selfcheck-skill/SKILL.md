---
name: selfcheck-skill
description: System health check for messaging channels and required tools
version: 1.0.0
tags: [system, health-check, diagnostics, messaging]
author: Kiro
created: 2026-05-02
---

# Selfcheck Skill

Comprehensive system health check to verify messaging channels and required tools are working properly.

## When to Use

- On startup or after configuration changes
- When messaging or media processing issues are suspected
- Before critical operations that depend on messaging or media tools
- Periodically as a maintenance check

## What This Checks

1. **Messaging Channels**
   - WhatsApp connectivity and configuration
   - Telegram connectivity and configuration
   - Any other configured chat channels in the future

2. **Required Tools**
   - ffmpeg (audio/video processing)
   - ImageMagick (image processing)

3. **Auto-Repair**
   - Attempts to install missing packages
   - Fixes common configuration issues
   - Reports what was fixed and what needs manual intervention

## Procedure

### 1. Run the selfcheck script

The script checks tools and WhatsApp bridge health:

```bash
python3 /opt/data/skills/selfcheck-skill/scripts/selfcheck.py
```

This will:
- Check ffmpeg and ImageMagick (auto-install if missing)
- Check WhatsApp bridge process and health endpoint
- Auto-start WhatsApp bridge if not running (npm install + node bridge.js)

### 2. Test Messaging Channels (Agent-level)

After the script completes, the agent MUST test actual message sending:

```python
# Test WhatsApp
try:
    send_message(target='whatsapp', message='✅ Selfcheck: WhatsApp operational')
    whatsapp_status = '✅ Working'
except Exception as e:
    whatsapp_status = f'❌ Failed: {e}'
    # If failed, try to repair WhatsApp bridge:
    # cd /opt/hermes/scripts/whatsapp-bridge
    # rm -rf node_modules
    # npm install --cache /tmp/npm-cache
    # node bridge.js (background)

# Test Telegram  
try:
    send_message(target='telegram', message='✅ Selfcheck: Telegram operational')
    telegram_status = '✅ Working'
except Exception as e:
    telegram_status = f'❌ Failed: {e}'
    # If failed, check Telegram bot token in config
```

**Expected output:**
- Messages successfully delivered to both platforms
- No connection errors

**If WhatsApp fails after bridge repair:**
- Check `/opt/hermes/scripts/whatsapp-bridge` exists
- Verify port 3000 is not blocked
- Check bridge logs for authentication issues

**If Telegram fails:**
- Verify Telegram bot token in `/opt/data/config.yaml`
- Check network connectivity
- Review Hermes gateway logs

### 3. Generate Final Report

Combine script output and messaging test results into a comprehensive report:

```
✅ SELFCHECK COMPLETE

TOOLS:
  ffmpeg: ✅ Working (v7.1.3)
  imagemagick: ✅ Working (v7.1.1-43)

MESSAGING:
  whatsapp_bridge: ✅ Running (health: {"status":"connected"})
  whatsapp: ✅ Message delivered
  telegram: ✅ Message delivered

🔧 AUTO-FIXED:
  - Started WhatsApp bridge

All systems operational.
```



## Example Implementation

```python
#!/usr/bin/env python3
import subprocess
import sys

results = {
    'messaging': {},
    'tools': {},
    'fixes': []
}

# Check messaging channels
print("🔍 Checking messaging channels...")
# Use send_message tool to list channels
# Parse output and check for WhatsApp and Telegram

# Check ffmpeg
print("🔍 Checking ffmpeg...")
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        results['tools']['ffmpeg'] = '✅ Working'
    else:
        raise Exception("ffmpeg check failed")
except:
    print("🔧 Installing ffmpeg...")
    subprocess.run(['apt-get', 'update'], check=True)
    subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'], check=True)
    results['fixes'].append('Installed ffmpeg')
    results['tools']['ffmpeg'] = '✅ Fixed'

# Check ImageMagick
print("🔍 Checking ImageMagick...")
try:
    result = subprocess.run(['magick', '-version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        results['tools']['imagemagick'] = '✅ Working'
    else:
        raise Exception("ImageMagick check failed")
except:
    try:
        result = subprocess.run(['convert', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            results['tools']['imagemagick'] = '✅ Working (legacy)'
        else:
            raise Exception("ImageMagick check failed")
    except:
        print("🔧 Installing ImageMagick...")
        subprocess.run(['apt-get', 'update'], check=True)
        subprocess.run(['apt-get', 'install', '-y', 'imagemagick'], check=True)
        results['fixes'].append('Installed ImageMagick')
        results['tools']['imagemagick'] = '✅ Fixed'

# Print report
print("\n" + "="*50)
print("SELFCHECK REPORT")
print("="*50)
for category, items in results.items():
    if category != 'fixes':
        print(f"\n{category.upper()}:")
        for name, status in items.items():
            print(f"  {name}: {status}")

if results['fixes']:
    print(f"\n🔧 AUTO-FIXED:")
    for fix in results['fixes']:
        print(f"  - {fix}")
```

## Pitfalls

- The script requires `send_message` tool access to check messaging channels
- ffmpeg and ImageMagick must be installed for tool checks to pass
- In Docker environments, use `python3` explicitly (not `python`) - the script has a proper shebang but manual invocation needs `python3 /path/to/script.py`
- WhatsApp gateway requires a separate service (`hermes-whatsapp`) running on port 3000 - if `send_message(action='list')` shows WhatsApp but sending fails with "Cannot connect to host localhost:3000", the gateway service is down
   - **Fix procedure**: `cd /opt/hermes/scripts/whatsapp-bridge && npm install --cache /tmp/npm-cache && node bridge.js` (run in background)
   - Check if already running: `ps aux | grep bridge.js` or `curl http://localhost:3000/health` (should return `{"status":"connected"}`)
   - If port 3000 already in use, the service is likely already running - verify with health check before attempting restart
   - In this environment, user `hermes` (uid 10000) can run apt-get

2. **Ephemeral State**
   - Container state is ephemeral
   - Installed packages won't persist across container rebuilds
   - Consider adding to Dockerfile for permanent fixes

3. **Network Issues**
   - Gateway services may be down temporarily
   - Check network connectivity before assuming configuration issues

4. **Version Compatibility**
   - ImageMagick 6.x uses `convert` command
   - ImageMagick 7.x uses `magick` command
   - Check both for compatibility

5. **Silent Failures**
   - Some tools may be installed but misconfigured
   - Test actual functionality, not just presence

## Success Criteria

- All messaging channels show "Connected ✓"
- ffmpeg and ImageMagick respond to version checks
- Test messages successfully delivered (if testing enabled)
- No manual intervention required

## Related Skills

- `hermes-agent` - For Hermes configuration and troubleshooting
- `telegram-gateway-setup` - For Telegram-specific configuration

## Reference Files

- `references/whatsapp-bridge-troubleshooting.md` - Detailed WhatsApp bridge startup, npm cache issues, and health check procedures

## Notes

- This skill should be run in a safe, non-production context first
- Auto-installation requires appropriate permissions
- Some fixes may require container restart to take effect
- Keep this skill updated as new channels or tools are added
