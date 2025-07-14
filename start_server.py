#!/usr/bin/env python3
"""
Quick start script for Meta Ads MCP Server

This script helps you get the Meta Ads MCP server running quickly.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("[INFO] Checking dependencies...")
    
    try:
        import meta_ads_mcp
        print("[OK] meta_ads_mcp package found")
        return True
    except ImportError:
        print("[ERROR] meta_ads_mcp package not found")
        print("   Please install it first:")
        print("   pip install -e .")
        return False

def setup_environment():
    """Help user set up environment variables"""
    print("\n[CONFIG] Environment Setup")
    print("-" * 30)
    
    # Check for Pipeboard token
    pipeboard_token = os.environ.get("PIPEBOARD_API_TOKEN")
    if pipeboard_token:
        print("[OK] PIPEBOARD_API_TOKEN found (recommended)")
        return True
    
    # Check for Meta app configuration
    meta_app_id = os.environ.get("META_APP_ID")
    meta_app_secret = os.environ.get("META_APP_SECRET")
    
    if meta_app_id:
        print(f"[OK] META_APP_ID found: {meta_app_id}")
        if meta_app_secret:
            print("[OK] META_APP_SECRET found")
        return True
    
    # No authentication found
    print("[WARNING] No authentication configured")
    print("\nChoose an authentication method:")
    print("1. Pipeboard (Recommended - Easy setup)")
    print("   - Sign up at https://pipeboard.co")
    print("   - Get API token and set: export PIPEBOARD_API_TOKEN=your_token")
    print("")
    print("2. Custom Meta App (Advanced)")
    print("   - Create app at https://developers.facebook.com/")
    print("   - Set: export META_APP_ID=your_app_id")
    print("")
    
    choice = input("Continue anyway? (y/N): ").lower().strip()
    return choice == 'y'

def run_server(args):
    """Run the MCP server"""
    print("\n[START] Starting Meta Ads MCP Server")
    print("=" * 40)
    
    # Build command
    cmd = [sys.executable, "-m", "meta_ads_mcp"]
    
    # Add transport option
    if args.http:
        cmd.extend(["--transport", "streamable-http"])
        if args.port:
            cmd.extend(["--port", str(args.port)])
        if args.host:
            cmd.extend(["--host", args.host])
    
    # Add app-id if provided
    if args.app_id:
        cmd.extend(["--app-id", args.app_id])
    
    # Add login flag if requested
    if args.login:
        cmd.append("--login")
    
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        if args.login:
            # Run login and return
            subprocess.run(cmd, check=True)
            print("[OK] Login completed!")
            return
        
        if args.http:
            print(f"[WEB] HTTP Server will start on http://{args.host or 'localhost'}:{args.port or 8080}")
            print("   Use this URL in your MCP client configuration")
        else:
            print("[STDIO] Starting in stdio mode for MCP clients")
            print("   Server will communicate via stdin/stdout")
        
        print("\n[RUN] Server starting... (Press Ctrl+C to stop)")
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n[STOP] Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Server failed to start: {e}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Quick start script for Meta Ads MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with stdio transport (for MCP clients)
  python start_server.py
  
  # Start with HTTP transport  
  python start_server.py --http --port 8080
  
  # Login first, then start server
  python start_server.py --login
  python start_server.py --http
  
  # Use custom Meta app
  python start_server.py --app-id YOUR_APP_ID --login
        """
    )
    
    parser.add_argument(
        "--http",
        action="store_true",
        help="Use HTTP transport instead of stdio"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for HTTP transport (default: 8080)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host for HTTP transport (default: localhost)"
    )
    
    parser.add_argument(
        "--app-id",
        type=str,
        help="Meta App ID for custom app authentication"
    )
    
    parser.add_argument(
        "--login",
        action="store_true",
        help="Perform login/authentication only"
    )
    
    args = parser.parse_args()
    
    print("[INFO] Meta Ads MCP Server - Quick Start")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n[ERROR] Environment setup cancelled")
        sys.exit(1)
    
    # Run the server
    run_server(args)

if __name__ == "__main__":
    main()
