#!/usr/bin/env python3
"""
Example HTTP client for testing the new Supabase video upload tools.
This demonstrates how to call the new MCP tools via HTTP when the server is running.
"""

import requests
import json

def test_mcp_video_tools():
    """Test the MCP video tools via HTTP."""
    
    # Configure the MCP server endpoint
    MCP_SERVER_URL = "http://localhost:8080"
    
    print("🎬 Testing Supabase Video Tools via MCP HTTP Server")
    print("=" * 60)
    
    # Test 1: List available videos in Supabase
    print("\n📋 1. Testing list_supabase_videos...")
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/list_supabase_videos",
            json={
                "arguments": {}
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Successfully retrieved Supabase video list")
            print("📊 Response preview:")
            content = json.loads(result.get('content', '{}'))
            if 'categories' in content:
                for category, info in content['categories'].items():
                    if 'total_videos' in info:
                        print(f"  - {category}: {info['total_videos']} videos")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error calling list_supabase_videos: {e}")
    
    # Test 2: Filter by Botox category
    print("\n📁 2. Testing category filter (Botox)...")
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/list_supabase_videos",
            json={
                "arguments": {
                    "category_filter": "Botox"
                }
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Successfully retrieved Botox videos")
            content = json.loads(result.get('content', '{}'))
            if 'category_data' in content and 'videos' in content['category_data']:
                print("📹 Available Botox videos:")
                for video in content['category_data']['videos']:
                    print(f"  - {video}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing category filter: {e}")
    
    # Test 3: Simulate video upload (this would need real credentials)
    print("\n🚀 3. Example of upload_video_from_supabase call...")
    print("⚠️  Note: This requires valid Meta Ads credentials")
    
    example_upload_request = {
        "arguments": {
            "account_id": "act_123456789",
            "supabase_video_path": "Botox/video/Uso_Botox_Correcto.mp4",
            "video_title": "Botox: Uso Correcto y Seguro"
        }
    }
    
    print("📝 Example request body:")
    print(json.dumps(example_upload_request, indent=2))
    
    # Test 4: Example of listing account videos
    print("\n📹 4. Example of list_account_videos call...")
    print("⚠️  Note: This requires valid Meta Ads credentials")
    
    example_list_request = {
        "arguments": {
            "account_id": "act_123456789",
            "limit": 10
        }
    }
    
    print("📝 Example request body:")
    print(json.dumps(example_list_request, indent=2))
    
    print("\n" + "=" * 60)
    print("🎯 Available MCP Tool Endpoints:")
    print(f"  - POST {MCP_SERVER_URL}/tools/list_supabase_videos")
    print(f"  - POST {MCP_SERVER_URL}/tools/upload_video_from_supabase")
    print(f"  - POST {MCP_SERVER_URL}/tools/list_account_videos")
    
    print("\n💡 To start the MCP server with HTTP transport:")
    print("  python -m meta_ads_mcp --transport streamable-http --port 8080")
    print("  OR")
    print("  python start_server.py --http --port 8080")

def main():
    """Run the HTTP client test."""
    test_mcp_video_tools()

if __name__ == "__main__":
    main()
