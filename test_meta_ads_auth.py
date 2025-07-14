#!/usr/bin/env python3
"""
Test script for Meta Ads MCP authentication

This script tests the authentication flow for the Meta Ads MCP server.
"""

import argparse
import sys
import os
import asyncio
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from meta_ads_mcp.core.auth import auth_manager, get_current_access_token, login as login_auth
from meta_ads_mcp.core.utils import logger
from meta_ads_mcp.core.api import make_api_request
from meta_ads_mcp.core.pipeboard_auth import pipeboard_auth_manager


async def test_authentication(app_id: str = None, force_login: bool = False):
    """Test the authentication flow"""
    
    print("[INFO] Testing Meta Ads MCP Authentication")
    print("=" * 50)
    
    # Set app_id if provided
    if app_id:
        print(f"Setting App ID: {app_id}")
        auth_manager.app_id = app_id
        os.environ["META_APP_ID"] = app_id
    
    # Force new login if requested
    if force_login:
        print("[REFRESH] Force login requested - clearing cached tokens")
        auth_manager.invalidate_token()
        pipeboard_auth_manager.clear_cached_token()
    
    # Check for Pipeboard authentication
    pipeboard_token = os.environ.get("PIPEBOARD_API_TOKEN")
    if pipeboard_token:
        print("[PIPEBOARD] Using Pipeboard authentication")
        try:
            access_token = pipeboard_auth_manager.get_access_token()
            if access_token:
                print("[OK] Pipeboard authentication successful")
                print(f"   Token prefix: {access_token[:10]}...")
            else:
                print("[ERROR] Pipeboard authentication failed")
                return False
        except Exception as e:
            print(f"[ERROR] Pipeboard authentication error: {e}")
            return False
    else:
        print("[OAUTH] Using direct Meta OAuth authentication")
        
        # Check if we have a cached token
        current_token = get_current_access_token()
        if current_token and not force_login:
            print("[OK] Found cached access token")
            print(f"   Token prefix: {current_token[:10]}...")
            access_token = current_token
        else:
            print("[WEB] Starting authentication flow...")
            try:
                login_auth()
                access_token = get_current_access_token()
                if access_token:
                    print("[OK] Authentication successful")
                    print(f"   Token prefix: {access_token[:10]}...")
                else:
                    print("[ERROR] Authentication failed - no token received")
                    return False
            except Exception as e:
                print(f"[ERROR] Authentication error: {e}")
                return False
    
    # Test API access
    print("\n[TEST] Testing API Access")
    print("-" * 30)
    
    try:
        # Test getting user's ad accounts
        print("[ACCOUNTS] Testing ad accounts access...")
        accounts_data = await make_api_request(
            "me/adaccounts",
            access_token,
            params={
                "fields": "id,name,account_status",
                "limit": 5
            }
        )
        
        if "error" in accounts_data:
            print(f"[ERROR] API Error: {accounts_data['error']}")
            return False
        
        if "data" in accounts_data:
            accounts = accounts_data["data"]
            print(f"[OK] Found {len(accounts)} ad accounts")
            for account in accounts[:3]:  # Show first 3
                print(f"   - {account.get('name', 'N/A')} ({account.get('id', 'N/A')})")
            if len(accounts) > 3:
                print(f"   ... and {len(accounts) - 3} more")
        else:
            print("[WARNING] No ad accounts found")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] API test error: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Test Meta Ads MCP authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_meta_ads_auth.py --app-id 1234567890
  python test_meta_ads_auth.py --app-id 1234567890 --force-login
  
Environment Variables:
  PIPEBOARD_API_TOKEN - Use Pipeboard authentication (recommended)
  META_APP_ID - Meta App ID for direct OAuth
  META_ACCESS_TOKEN - Direct access token (bypasses authentication)
        """
    )
    
    parser.add_argument(
        "--app-id",
        type=str,
        help="Meta App ID for authentication"
    )
    
    parser.add_argument(
        "--force-login",
        action="store_true",
        help="Force a new login even if cached token exists"
    )
    
    args = parser.parse_args()
    
    # Run the async test
    try:
        success = asyncio.run(test_authentication(args.app_id, args.force_login))
        
        print("\n" + "=" * 50)
        if success:
            print("[SUCCESS] Authentication test PASSED!")
            print("   Your Meta Ads MCP is ready to use.")
            sys.exit(0)
        else:
            print("[FAIL] Authentication test FAILED!")
            print("   Please check your configuration and try again.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[WARNING] Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
