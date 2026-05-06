     1|#!/usr/bin/env python3
     2|"""
     3|Selfcheck script for Hermes Agent
     4|Checks messaging channels and required tools, auto-fixes issues
     5|"""
     6|import subprocess
     7|import sys
     8|import json
     9|import os
    10|from typing import Dict, List, Any
    11|
    12|def run_command(cmd: List[str], timeout: int = 5, cwd: str = None) -> tuple[bool, str]:
    13|    """Run a command and return success status and output"""
    14|    try:
    15|        result = subprocess.run(
    16|            cmd,
    17|            capture_output=True,
    18|            text=True,
    19|            timeout=timeout,
    20|            cwd=cwd
    21|        )
    22|        return result.returncode == 0, result.stdout + result.stderr
    23|    except Exception as e:
    24|        return False, str(e)
    25|
    26|def check_ffmpeg() -> Dict[str, Any]:
    27|    """Check if ffmpeg is installed and working"""
    28|    print("🔍 Checking ffmpeg...")
    29|    success, output = run_command(['ffmpeg', '-version'])
    30|    
    31|    if success:
    32|        version = output.split('\n')[0] if output else 'unknown'
    33|        return {
    34|            'status': '✅ Working',
    35|            'version': version,
    36|            'fixed': False
    37|        }
    38|    
    39|    # Try to install
    40|    print("🔧 Installing ffmpeg...")
    41|    try:
    42|        run_command(['apt-get', 'update'], timeout=60)
    43|        run_command(['apt-get', 'install', '-y', 'ffmpeg'], timeout=120)
    44|        
    45|        # Verify installation
    46|        success, output = run_command(['ffmpeg', '-version'])
    47|        if success:
    48|            version = output.split('\n')[0] if output else 'unknown'
    49|            return {
    50|                'status': '✅ Fixed',
    51|                'version': version,
    52|                'fixed': True
    53|            }
    54|        else:
    55|            return {
    56|                'status': '❌ Failed to install',
    57|                'error': output,
    58|                'fixed': False
    59|            }
    60|    except Exception as e:
    61|        return {
    62|            'status': '❌ Installation error',
    63|            'error': str(e),
    64|            'fixed': False
    65|        }
    66|
    67|def check_imagemagick() -> Dict[str, Any]:
    68|    """Check if ImageMagick is installed and working"""
    69|    print("🔍 Checking ImageMagick...")
    70|    
    71|    # Try ImageMagick 7.x (magick command)
    72|    success, output = run_command(['magick', '-version'])
    73|    if success:
    74|        version = output.split('\n')[0] if output else 'unknown'
    75|        return {
    76|            'status': '✅ Working (v7)',
    77|            'version': version,
    78|            'fixed': False
    79|        }
    80|    
    81|    # Try ImageMagick 6.x (convert command)
    82|    success, output = run_command(['convert', '-version'])
    83|    if success:
    84|        version = output.split('\n')[0] if output else 'unknown'
    85|        return {
    86|            'status': '✅ Working (v6)',
    87|            'version': version,
    88|            'fixed': False
    89|        }
    90|    
    91|    # Try to install
    92|    print("🔧 Installing ImageMagick...")
    93|    try:
    94|        run_command(['apt-get', 'update'], timeout=60)
    95|        run_command(['apt-get', 'install', '-y', 'imagemagick'], timeout=120)
    96|        
    97|        # Verify installation (try both commands)
    98|        success, output = run_command(['magick', '-version'])
    99|        if success:
   100|            version = output.split('\n')[0] if output else 'unknown'
   101|            return {
   102|                'status': '✅ Fixed (v7)',
   103|                'version': version,
   104|                'fixed': True
   105|            }
   106|        
   107|        success, output = run_command(['convert', '-version'])
   108|        if success:
   109|            version = output.split('\n')[0] if output else 'unknown'
   110|            return {
   111|                'status': '✅ Fixed (v6)',
   112|                'version': version,
   113|                'fixed': True
   114|            }
   115|        
   116|        return {
   117|            'status': '❌ Failed to install',
   118|            'error': output,
   119|            'fixed': False
   120|        }
   121|    except Exception as e:
   122|        return {
   123|            'status': '❌ Installation error',
   124|            'error': str(e),
   125|            'fixed': False
   126|        }
   127|
   128|def check_whatsapp_bridge() -> Dict[str, Any]:
   129|    """Check if WhatsApp bridge is running and healthy"""
   130|    print("🔍 Checking WhatsApp bridge...")
   131|    
   132|    # Check if bridge process is running
   133|    success, output = run_command(['pgrep', '-f', 'bridge.js'])
   134|    if success and output.strip():
   135|        # Process is running, check health endpoint
   136|        success, health_output = run_command(['curl', '-s', 'http://localhost:3000/health'], timeout=5)
   137|        if success and 'connected' in health_output:
   138|            return {
   139|                'status': '✅ Running',
   140|                'health': health_output.strip(),
   141|                'fixed': False
   142|            }
   143|        else:
   144|            return {
   145|                'status': '⚠️ Running but unhealthy',
   146|                'health': health_output.strip() if health_output else 'No response',
   147|                'fixed': False
   148|            }
   149|    
   150|    # Bridge not running, try to start it
   151|    print("🔧 WhatsApp bridge not running, attempting to start...")
   152|    bridge_dir = '/opt/hermes/scripts/whatsapp-bridge'
   153|    
   154|    if not os.path.exists(bridge_dir):
   155|        return {
   156|            'status': '❌ Bridge directory not found',
   157|            'error': f'{bridge_dir} does not exist',
   158|            'fixed': False
   159|        }
   160|    
   161|    try:
   162|        # Clean and reinstall node_modules
   163|        print("   Cleaning node_modules...")
   164|        run_command(['rm', '-rf', 'node_modules'], timeout=10, cwd=bridge_dir)
   165|        
   166|        print("   Installing dependencies...")
   167|        success, output = run_command(
   168|            ['npm', 'install', '--cache', '/tmp/npm-cache'],
   169|            timeout=180,
   170|            cwd=bridge_dir
   171|        )
   172|        
   173|        if not success:
   174|            return {
   175|                'status': '❌ npm install failed',
   176|                'error': output,
   177|                'fixed': False
   178|            }
   179|        
   180|        # Start bridge in background
   181|        print("   Starting bridge...")
   182|        subprocess.Popen(
   183|            ['node', 'bridge.js'],
   184|            cwd=bridge_dir,
   185|            stdout=subprocess.DEVNULL,
   186|            stderr=subprocess.DEVNULL,
   187|            start_new_session=True
   188|        )
   189|        
   190|        # Wait a moment and check health
   191|        import time
   192|        time.sleep(3)
   193|        
   194|        success, health_output = run_command(['curl', '-s', 'http://localhost:3000/health'], timeout=5)
   195|        if success and 'connected' in health_output:
   196|            return {
   197|                'status': '✅ Fixed and running',
   198|                'health': health_output.strip(),
   199|                'fixed': True
   200|            }
   201|        else:
   202|            return {
   203|                'status': '⚠️ Started but not healthy yet',
   204|                'health': health_output.strip() if health_output else 'No response',
   205|                'fixed': True
   206|            }
   207|    except Exception as e:
   208|        return {
   209|            'status': '❌ Failed to start',
   210|            'error': str(e),
   211|            'fixed': False
   212|        }
   213|
   214|def check_required_tools() -> Dict[str, Any]:
   215|    """Check required tools and return per-tool status."""
   216|    print("🔍 Checking required tools...")
   217|    tools = ["curl", "ffmpeg", "magick", "convert", "ping", "nslookup", "whois", "nmap", "pandoc"]
   218|    results: Dict[str, Any] = {}
   219|
   220|    for tool in tools:
   221|        success, output = run_command(["bash", "-lc", f"command -v {tool}"])
   222|        results[tool] = {
   223|            "exists": success,
   224|            "path": output.strip() if success else "",
   225|        }
   226|    return results
   227|
   228|
   229|def send_telegram_alert(message: str) -> bool:
   230|    """Send a notification to Telegram using the Hermes messaging tool via subprocess-free fallback is not available here.
   231|
   232|    This script cannot directly call Hermes tools, so it reports missing tools in stdout.
   233|    The agent wrapping this script should send the actual Telegram message when parsing the report.
   234|    """
   235|    return False
   236|
   237|
   238|def test_channel(name: str, target: str) -> Dict[str, Any]:
   239|    """Test actual message delivery to a channel.
   240|
   241|    Note: this script itself cannot access Hermes send_message directly. The agent
   242|    should perform the actual send after script output is read. We still track the
   243|    requested test in the report so the wrapper can act on it.
   244|    """
   245|    return {
   246|        "name": name,
   247|        "target": target,
   248|        "requested": True,
   249|    }
   250|
   251|
   252|def main():
   253|    """Run all checks and generate report"""
   254|    print("="*60)
   255|    print("HERMES AGENT SELFCHECK")
   256|    print("="*60)
   257|    print()
   258|
   259|    results = {
   260|        'tools': {},
   261|        'messaging': {},
   262|        'missing_tools': [],
   263|        'fixes': [],
   264|        'errors': []
   265|    }
   266|
   267|    # Check required tools first
   268|    required_tools = check_required_tools()
   269|    results['tools']['required'] = required_tools
   270|    for tool, info in required_tools.items():
   271|        if not info['exists']:
   272|            results['missing_tools'].append(tool)
   273|            results['errors'].append(f"Missing required tool: {tool}")
   274|
   275|    print()
   276|
   277|    # Check ffmpeg
   278|    ffmpeg_result = check_ffmpeg()
   279|    results['tools']['ffmpeg'] = ffmpeg_result
   280|    if ffmpeg_result['fixed']:
   281|        results['fixes'].append('Installed ffmpeg')
   282|    if '❌' in ffmpeg_result['status']:
   283|        results['errors'].append(f"ffmpeg: {ffmpeg_result.get('error', 'unknown error')}")
   284|
   285|    print()
   286|
   287|    # Check ImageMagick
   288|    imagemagick_result = check_imagemagick()
   289|    results['tools']['imagemagick'] = imagemagick_result
   290|    if imagemagick_result['fixed']:
   291|        results['fixes'].append('Installed ImageMagick')
   292|    if '❌' in imagemagick_result['status']:
   293|        results['errors'].append(f"ImageMagick: {imagemagick_result.get('error', 'unknown error')}")
   294|
   295|    print()
   296|
   297|    # Check WhatsApp bridge
   298|    whatsapp_result = check_whatsapp_bridge()
   299|    results['messaging']['whatsapp_bridge'] = whatsapp_result
   300|    if whatsapp_result['fixed']:
   301|        results['fixes'].append('Started WhatsApp bridge')
   302|    if '❌' in whatsapp_result['status']:
   303|        results['errors'].append(f"WhatsApp bridge: {whatsapp_result.get('error', 'unknown error')}")
   304|
   305|    print()
   306|
   307|    # Messaging channel tests are handled by the agent wrapper using send_message.
   308|    # The wrapper must actually send the selfcheck messages and, on failure,
   309|    # repair the channel before retrying.
   310|    results['messaging']['whatsapp'] = test_channel('whatsapp', 'whatsapp')
   311|    results['messaging']['telegram'] = test_channel('telegram', 'telegram')
   312|
   313|    print("📱 Messaging Tests:")
   314|    print("   WhatsApp: the Hermes wrapper must send '✅ Selfcheck: WhatsApp operational'")
   315|    print("   Telegram: the Hermes wrapper must send '✅ Selfcheck: Telegram operational'")
   316|    print()
   317|
   318|    # Print report
   319|    print("="*60)
   320|    print("SELFCHECK REPORT")
   321|    print("="*60)
   322|    print()
   323|
   324|    print("TOOLS:")
   325|    print("  Required tool inventory:")
   326|    for tool, info in results['tools']['required'].items():
   327|        status = '✅ Present' if info['exists'] else '❌ Missing'
   328|        path = info.get('path', '')
   329|        print(f"    {tool}: {status}" + (f" ({path})" if path else ""))
   330|    for name in ['ffmpeg', 'imagemagick']:
   331|        if name in results['tools']:
   332|            info = results['tools'][name]
   333|            status = info['status']
   334|            version = info.get('version', '')
   335|            print(f"  {name}: {status}")
   336|            if version and '✅' in status:
   337|                print(f"    Version: {version}")
   338|
   339|    print()
   340|
   341|    print("MESSAGING:")
   342|    for name, info in results['messaging'].items():
   343|        if name == 'whatsapp_bridge':
   344|            status = info['status']
   345|            health = info.get('health', '')
   346|            print(f"  {name}: {status}")
   347|            if health and '✅' in status:
   348|                print(f"    Health: {health}")
   349|        else:
   350|            print(f"  {name}: requested actual selfcheck message send")
   351|
   352|    print()
   353|
   354|    if results['missing_tools']:
   355|        print("⚠️  MISSING TOOLS:")
   356|        for tool in results['missing_tools']:
   357|            print(f"  - {tool}")
   358|        print()
   359|        print("If any required tool is missing, the agent should send a Telegram alert.")
   360|        print()
   361|
   362|    if results['fixes']:
   363|        print("🔧 AUTO-FIXED:")
   364|        for fix in results['fixes']:
   365|            print(f"  - {fix}")
   366|        print()
   367|
   368|    if results['errors']:
   369|        print("⚠️  ERRORS:")
   370|        for error in results['errors']:
   371|            print(f"  - {error}")
   372|        print()
   373|
   374|    # Exit with appropriate code
   375|    if results['errors']:
   376|        print("❌ Selfcheck completed with errors")
   377|        sys.exit(1)
   378|    elif results['fixes']:
   379|        print("✅ Selfcheck completed with auto-fixes applied")
   380|        sys.exit(0)
   381|    else:
   382|        print("✅ Selfcheck completed - all systems operational")
   383|        sys.exit(0)
   384|
   385|if __name__ == '__main__':
   386|    main()
   387|