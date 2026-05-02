#!/usr/bin/env python3
"""
Selfcheck script for Hermes Agent
Checks messaging channels and required tools, auto-fixes issues
"""
import subprocess
import sys
import json
import os
from typing import Dict, List, Any

def run_command(cmd: List[str], timeout: int = 5, cwd: str = None) -> tuple[bool, str]:
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def check_ffmpeg() -> Dict[str, Any]:
    """Check if ffmpeg is installed and working"""
    print("🔍 Checking ffmpeg...")
    success, output = run_command(['ffmpeg', '-version'])
    
    if success:
        version = output.split('\n')[0] if output else 'unknown'
        return {
            'status': '✅ Working',
            'version': version,
            'fixed': False
        }
    
    # Try to install
    print("🔧 Installing ffmpeg...")
    try:
        run_command(['apt-get', 'update'], timeout=60)
        run_command(['apt-get', 'install', '-y', 'ffmpeg'], timeout=120)
        
        # Verify installation
        success, output = run_command(['ffmpeg', '-version'])
        if success:
            version = output.split('\n')[0] if output else 'unknown'
            return {
                'status': '✅ Fixed',
                'version': version,
                'fixed': True
            }
        else:
            return {
                'status': '❌ Failed to install',
                'error': output,
                'fixed': False
            }
    except Exception as e:
        return {
            'status': '❌ Installation error',
            'error': str(e),
            'fixed': False
        }

def check_imagemagick() -> Dict[str, Any]:
    """Check if ImageMagick is installed and working"""
    print("🔍 Checking ImageMagick...")
    
    # Try ImageMagick 7.x (magick command)
    success, output = run_command(['magick', '-version'])
    if success:
        version = output.split('\n')[0] if output else 'unknown'
        return {
            'status': '✅ Working (v7)',
            'version': version,
            'fixed': False
        }
    
    # Try ImageMagick 6.x (convert command)
    success, output = run_command(['convert', '-version'])
    if success:
        version = output.split('\n')[0] if output else 'unknown'
        return {
            'status': '✅ Working (v6)',
            'version': version,
            'fixed': False
        }
    
    # Try to install
    print("🔧 Installing ImageMagick...")
    try:
        run_command(['apt-get', 'update'], timeout=60)
        run_command(['apt-get', 'install', '-y', 'imagemagick'], timeout=120)
        
        # Verify installation (try both commands)
        success, output = run_command(['magick', '-version'])
        if success:
            version = output.split('\n')[0] if output else 'unknown'
            return {
                'status': '✅ Fixed (v7)',
                'version': version,
                'fixed': True
            }
        
        success, output = run_command(['convert', '-version'])
        if success:
            version = output.split('\n')[0] if output else 'unknown'
            return {
                'status': '✅ Fixed (v6)',
                'version': version,
                'fixed': True
            }
        
        return {
            'status': '❌ Failed to install',
            'error': output,
            'fixed': False
        }
    except Exception as e:
        return {
            'status': '❌ Installation error',
            'error': str(e),
            'fixed': False
        }

def check_whatsapp_bridge() -> Dict[str, Any]:
    """Check if WhatsApp bridge is running and healthy"""
    print("🔍 Checking WhatsApp bridge...")
    
    # Check if bridge process is running
    success, output = run_command(['pgrep', '-f', 'bridge.js'])
    if success and output.strip():
        # Process is running, check health endpoint
        success, health_output = run_command(['curl', '-s', 'http://localhost:3000/health'], timeout=5)
        if success and 'connected' in health_output:
            return {
                'status': '✅ Running',
                'health': health_output.strip(),
                'fixed': False
            }
        else:
            return {
                'status': '⚠️ Running but unhealthy',
                'health': health_output.strip() if health_output else 'No response',
                'fixed': False
            }
    
    # Bridge not running, try to start it
    print("🔧 WhatsApp bridge not running, attempting to start...")
    bridge_dir = '/opt/hermes/scripts/whatsapp-bridge'
    
    if not os.path.exists(bridge_dir):
        return {
            'status': '❌ Bridge directory not found',
            'error': f'{bridge_dir} does not exist',
            'fixed': False
        }
    
    try:
        # Clean and reinstall node_modules
        print("   Cleaning node_modules...")
        run_command(['rm', '-rf', 'node_modules'], timeout=10, cwd=bridge_dir)
        
        print("   Installing dependencies...")
        success, output = run_command(
            ['npm', 'install', '--cache', '/tmp/npm-cache'],
            timeout=180,
            cwd=bridge_dir
        )
        
        if not success:
            return {
                'status': '❌ npm install failed',
                'error': output,
                'fixed': False
            }
        
        # Start bridge in background
        print("   Starting bridge...")
        subprocess.Popen(
            ['node', 'bridge.js'],
            cwd=bridge_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        # Wait a moment and check health
        import time
        time.sleep(3)
        
        success, health_output = run_command(['curl', '-s', 'http://localhost:3000/health'], timeout=5)
        if success and 'connected' in health_output:
            return {
                'status': '✅ Fixed and running',
                'health': health_output.strip(),
                'fixed': True
            }
        else:
            return {
                'status': '⚠️ Started but not healthy yet',
                'health': health_output.strip() if health_output else 'No response',
                'fixed': True
            }
    except Exception as e:
        return {
            'status': '❌ Failed to start',
            'error': str(e),
            'fixed': False
        }

def main():
    """Run all checks and generate report"""
    print("="*60)
    print("HERMES AGENT SELFCHECK")
    print("="*60)
    print()
    
    results = {
        'tools': {},
        'messaging': {},
        'fixes': [],
        'errors': []
    }
    
    # Check ffmpeg
    ffmpeg_result = check_ffmpeg()
    results['tools']['ffmpeg'] = ffmpeg_result
    if ffmpeg_result['fixed']:
        results['fixes'].append('Installed ffmpeg')
    if '❌' in ffmpeg_result['status']:
        results['errors'].append(f"ffmpeg: {ffmpeg_result.get('error', 'unknown error')}")
    
    print()
    
    # Check ImageMagick
    imagemagick_result = check_imagemagick()
    results['tools']['imagemagick'] = imagemagick_result
    if imagemagick_result['fixed']:
        results['fixes'].append('Installed ImageMagick')
    if '❌' in imagemagick_result['status']:
        results['errors'].append(f"ImageMagick: {imagemagick_result.get('error', 'unknown error')}")
    
    print()
    
    # Check WhatsApp bridge
    whatsapp_result = check_whatsapp_bridge()
    results['messaging']['whatsapp_bridge'] = whatsapp_result
    if whatsapp_result['fixed']:
        results['fixes'].append('Started WhatsApp bridge')
    if '❌' in whatsapp_result['status']:
        results['errors'].append(f"WhatsApp bridge: {whatsapp_result.get('error', 'unknown error')}")
    
    print()
    
    # Note about messaging tests
    print("📱 Messaging Tests:")
    print("   The agent will test actual message sending to WhatsApp and Telegram")
    print("   after this script completes.")
    print()
    
    # Print report
    print("="*60)
    print("SELFCHECK REPORT")
    print("="*60)
    print()
    
    print("TOOLS:")
    for name, info in results['tools'].items():
        status = info['status']
        version = info.get('version', '')
        print(f"  {name}: {status}")
        if version and '✅' in status:
            print(f"    Version: {version}")
    
    print()
    
    print("MESSAGING:")
    for name, info in results['messaging'].items():
        status = info['status']
        health = info.get('health', '')
        print(f"  {name}: {status}")
        if health and '✅' in status:
            print(f"    Health: {health}")
    
    print()
    
    if results['fixes']:
        print("🔧 AUTO-FIXED:")
        for fix in results['fixes']:
            print(f"  - {fix}")
        print()
    
    if results['errors']:
        print("⚠️  ERRORS:")
        for error in results['errors']:
            print(f"  - {error}")
        print()
    
    # Exit with appropriate code
    if results['errors']:
        print("❌ Selfcheck completed with errors")
        sys.exit(1)
    elif results['fixes']:
        print("✅ Selfcheck completed with auto-fixes applied")
        sys.exit(0)
    else:
        print("✅ Selfcheck completed - all systems operational")
        sys.exit(0)

if __name__ == '__main__':
    main()
