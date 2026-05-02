# Selfcheck Skill

**System health check for messaging channels and required tools**

## Overview

Comprehensive automated health check that verifies messaging channels (WhatsApp, Telegram) and required tools (ffmpeg, ImageMagick) are working properly. Includes auto-repair capabilities for common issues.

## Features

- ✅ **Tool Verification**: Checks ffmpeg and ImageMagick, auto-installs if missing
- ✅ **WhatsApp Bridge Health**: Detects and auto-repairs WhatsApp bridge issues
- ✅ **Actual Message Testing**: Sends test messages to verify end-to-end functionality
- ✅ **Auto-Repair**: Automatically fixes common issues without manual intervention
- ✅ **Comprehensive Reporting**: Clear status for all components with detailed diagnostics

## What It Checks

1. **Tools**
   - ffmpeg (audio/video processing)
   - ImageMagick (image processing)
   - Auto-installs missing packages

2. **WhatsApp Bridge**
   - Process health check
   - HTTP health endpoint verification
   - Auto-restart with npm dependency reinstall if needed

3. **Messaging Channels**
   - WhatsApp message delivery test
   - Telegram message delivery test
   - End-to-end verification

## Usage

Load the skill and run the selfcheck:

```
Load selfcheck-skill and run a complete system health check
```

The agent will:
1. Run the Python selfcheck script to verify tools and WhatsApp bridge
2. Test actual message sending to WhatsApp and Telegram
3. Generate a comprehensive status report

## Auto-Repair Capabilities

- **Missing Tools**: Automatically installs ffmpeg or ImageMagick via apt-get
- **WhatsApp Bridge Down**: Cleans node_modules, reinstalls dependencies, and starts the bridge
- **Port Conflicts**: Detects if bridge is already running before attempting restart

## Requirements

- Docker environment with apt-get access
- WhatsApp bridge at `/opt/hermes/scripts/whatsapp-bridge`
- Node.js and npm installed
- Hermes messaging gateway configured

## Files

- `SKILL.md` - Complete skill documentation with procedures and pitfalls
- `scripts/selfcheck.py` - Python script for tool and bridge health checks
- `references/whatsapp-bridge-troubleshooting.md` - Detailed WhatsApp bridge troubleshooting guide

## Example Output

```
✅ SELFCHECK COMPLETE - ALL SYSTEMS OPERATIONAL

TOOLS:
  ffmpeg: ✅ Working (v7.1.3-0+deb13u1)
  ImageMagick: ✅ Working (v7.1.1-43)

MESSAGING:
  WhatsApp Bridge: ✅ Running (health: connected, uptime: 391s)
  WhatsApp: ✅ Message delivered
  Telegram: ✅ Message delivered

🔧 AUTO-FIXED:
  - Started WhatsApp bridge

All systems operational.
```

## Provenance

- **Author**: Kiro (Hermes Agent)
- **Created**: 2026-05-02
- **Version**: 1.1.0
- **Tested**: Hermes Agent Docker environment
- **License**: MIT

## Notes

- Designed for ephemeral Docker environments where packages may need reinstallation
- WhatsApp bridge auto-repair uses `/tmp/npm-cache` to avoid permission issues
- Script exits with code 0 (success), 1 (errors), appropriate for cron job monitoring
- Recommended to run on startup via cron job for proactive health monitoring
