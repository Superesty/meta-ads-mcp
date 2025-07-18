#!/usr/bin/env python3
"""
Test script for the new Supabase video upload functionality.
This script demonstrates how to use the new MCP tools to upload videos from Supabase to Meta Ads.
"""

import asyncio
import json
from meta_ads_mcp.core.ads_library import (
    list_supabase_videos,
    upload_video_from_supabase,
    list_account_videos
)

async def test_supabase_video_tools():
    """Test the new Supabase video integration tools."""
    
    print("🎬 Testing Supabase Video Upload Tools for Meta Ads MCP")
    print("=" * 60)
    
    # Test 1: List available videos in Supabase
    print("\n📋 1. Listing available videos in Supabase bucket...")
    try:
        videos_result = await list_supabase_videos()
        videos_data = json.loads(videos_result)
        print("✅ Successfully retrieved Supabase video list")
        print(f"📊 Total categories: {len(videos_data['categories'])}")
        
        for category, info in videos_data['categories'].items():
            if 'total_videos' in info:
                print(f"  - {category}: {info['total_videos']} videos")
    except Exception as e:
        print(f"❌ Error listing Supabase videos: {e}")
    
    # Test 2: List videos in a specific category
    print("\n📁 2. Listing Botox category videos...")
    try:
        botox_result = await list_supabase_videos(category_filter="Botox")
        botox_data = json.loads(botox_result)
        print("✅ Successfully retrieved Botox videos")
        if 'category_data' in botox_data and 'videos' in botox_data['category_data']:
            for video in botox_data['category_data']['videos']:
                print(f"  - {video}")
    except Exception as e:
        print(f"❌ Error listing Botox videos: {e}")
    
    # Test 3: Simulate video upload (without actual API call)
    print("\n🚀 3. Simulating video upload to Meta Ads...")
    print("⚠️  Note: This would require a valid Meta Ads access token and account ID")
    print("Example usage:")
    print("""
    result = await upload_video_from_supabase(
        account_id="act_123456789",
        supabase_video_path="Botox/video/Uso_Botox_Correcto.mp4",
        video_title="Uso Correcto del Botox - Video Educativo"
    )
    """)
    
    # Test 4: Show how to list account videos
    print("\n📹 4. Example of listing account videos in Meta Ads...")
    print("⚠️  Note: This would require a valid Meta Ads access token and account ID")
    print("Example usage:")
    print("""
    result = await list_account_videos(
        account_id="act_123456789",
        limit=10
    )
    """)
    
    print("\n" + "=" * 60)
    print("🎯 Summary of New MCP Tools:")
    print("  1. list_supabase_videos() - List available videos in Cogitia bucket")
    print("  2. upload_video_from_supabase() - Upload video to Meta Ads Library")
    print("  3. list_account_videos() - List videos in Meta Ads account")
    print("\n💡 Integration Benefits:")
    print("  - Direct video transfer from Cogitia content to Meta Ads")
    print("  - Automated content workflow for medical/aesthetic campaigns")
    print("  - No manual download/upload process needed")
    print("  - Maintains video quality and metadata")

def main():
    """Run the test."""
    asyncio.run(test_supabase_video_tools())

if __name__ == "__main__":
    main()
