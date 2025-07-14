#!/usr/bin/env python3
"""
Test script to verify that the serialization fix works correctly
"""

import asyncio
import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_get_campaigns_serialization():
    """Test that get_campaigns returns a JSON string, not a dict"""
    print("🧪 Testing get_campaigns serialization...")
    
    try:
        from meta_ads_mcp.core.campaigns import get_campaigns
        print("✅ Successfully imported get_campaigns")
        
        # Test with a real account ID
        result = await get_campaigns(account_id='act_1127960206038936', limit=3)
        
        print(f"📊 Result type: {type(result)}")
        print(f"📊 Is string?: {isinstance(result, str)}")
        
        if isinstance(result, str):
            print("✅ Returned a string (correct for MCP)")
            try:
                parsed = json.loads(result)
                print("✅ String is valid JSON")
                
                if 'data' in parsed:
                    print(f"✅ Found campaigns data: {len(parsed['data'])} campaigns")
                elif 'error' in parsed:
                    print(f"⚠️  Error in response: {parsed['error']}")
                else:
                    print(f"❓ Unexpected response structure: {list(parsed.keys())}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ String is not valid JSON: {e}")
                print(f"Raw result: {result[:200]}...")
        else:
            print("❌ Returned a dict (WRONG for MCP - this causes the Pydantic error)")
            print(f"Raw result: {result}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

async def test_error_handling():
    """Test that error cases also return JSON strings"""
    print("\n🧪 Testing error case serialization...")
    
    try:
        from meta_ads_mcp.core.campaigns import get_campaigns
        
        # Test with invalid account ID to trigger error
        result = await get_campaigns(account_id='invalid_account', limit=3)
        
        print(f"📊 Error result type: {type(result)}")
        print(f"📊 Is string?: {isinstance(result, str)}")
        
        if isinstance(result, str):
            print("✅ Error returned as string (correct)")
            try:
                parsed = json.loads(result)
                print("✅ Error response is valid JSON")
                if 'error' in parsed:
                    print(f"✅ Error properly structured: {parsed['error']}")
            except json.JSONDecodeError:
                print("❌ Error response is not valid JSON")
        else:
            print("❌ Error returned as dict (WRONG - this would cause Pydantic error)")
            
    except Exception as e:
        print(f"❌ Error during error test: {e}")

if __name__ == "__main__":
    print("🔧 Meta Ads MCP Serialization Fix Test")
    print("=" * 50)
    
    asyncio.run(test_get_campaigns_serialization())
    asyncio.run(test_error_handling())
    
    print("\n" + "=" * 50)
    print("📋 Test completed!")
    print("\n💡 If all tests show ✅, the serialization fix is working.")
    print("💡 If you see ❌ dict results, there are still serialization issues.")
