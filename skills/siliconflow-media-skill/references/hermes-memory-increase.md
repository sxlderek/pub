# Increasing Hermes Memory Limits

## Problem

Hermes has default memory limits that can fill up quickly:
- Agent memory (notes): 2,200 characters
- User profile: 1,375 characters

When memory is full, you cannot save new information without removing old entries.

## Solution

Edit the config file to increase memory limits permanently.

## Location

Config file: `/opt/data/config.yaml`

This location is bind-mounted to the host, so changes persist across container restarts and upgrades.

## Steps

1. **Backup the config:**
   ```bash
   cp /opt/data/config.yaml /opt/data/config.yaml.backup.$(date +%Y%m%d_%H%M%S)
   ```

2. **Edit memory limits:**
   ```bash
   # Example: 10x increase
   sed -i 's/memory_char_limit: 2200/memory_char_limit: 22000/' /opt/data/config.yaml
   sed -i 's/user_char_limit: 1375/user_char_limit: 13750/' /opt/data/config.yaml
   ```

3. **Verify changes:**
   ```bash
   grep -A 3 "^memory:" /opt/data/config.yaml
   ```

4. **Restart session** for changes to take effect

## Config Structure

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 22000      # Agent notes
  user_char_limit: 13750         # User profile
  provider: ''
  nudge_interval: 10
  flush_min_turns: 6
```

## Persistence

✅ Changes persist across:
- Container restarts
- Container upgrades
- Session restarts

The config is in `/opt/data/` which is bind-mounted to the host filesystem.

## Session Notes

- Discovered 2026-05-02
- User requested 10x memory increase
- Successfully increased from 2,200 → 22,000 (agent) and 1,375 → 13,750 (user)
- Backup created at `/opt/data/config.yaml.backup.20260502_162021`
