#!/usr/bin/env python3
"""
Example usage script for YouTube Metadata Extractor

This script demonstrates different ways to use the YouTubeMetadataExtractor class.
"""

import os
import sys
from datetime import datetime
from youtube_metadata_extractor import YouTubeMetadataExtractor

# Try to import config file, fallback to manual configuration
try:
    from config import (
        YOUTUBE_API_KEY, CHANNEL_ID, USERNAME, MAX_RESULTS,
        MAX_RETRIES, RETRY_DELAY, OUTPUT_FILENAME
    )
    print("✅ Loaded configuration from config.py")
except ImportError:
    print("ℹ️  No config.py found, using manual configuration")
    # Manual configuration - REPLACE WITH YOUR VALUES
    YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"
    CHANNEL_ID = "YOUR_CHANNEL_ID_HERE"  # Or set to None if using USERNAME
    USERNAME = None  # Or set your username if not using CHANNEL_ID
    MAX_RESULTS = None  # None for all videos, or set a number to limit
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    OUTPUT_FILENAME = None


def validate_configuration():
    """Validate that configuration is properly set."""
    if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY_HERE" or not YOUTUBE_API_KEY:
        print("❌ Error: YouTube API key not configured")
        print("Please either:")
        print("  1. Copy config_example.py to config.py and update it with your values")
        print("  2. Update the manual configuration in this script")
        print("\n📚 See README.md for instructions on obtaining an API key")
        return False
    
    if ((CHANNEL_ID == "YOUR_CHANNEL_ID_HERE" or not CHANNEL_ID) and 
        (not USERNAME)):
        print("❌ Error: Neither channel ID nor username configured")
        print("Please set either CHANNEL_ID or USERNAME in your configuration")
        return False
    
    return True


def example_basic_extraction():
    """Example 1: Basic metadata extraction"""
    print("\n" + "="*60)
    print("📋 EXAMPLE 1: Basic Metadata Extraction")
    print("="*60)
    
    if not validate_configuration():
        return
    
    try:
        # Initialize extractor
        extractor = YouTubeMetadataExtractor(
            api_key=YOUTUBE_API_KEY,
            max_retries=MAX_RETRIES,
            retry_delay=RETRY_DELAY
        )
        
        # Extract metadata
        print("🔍 Extracting video metadata...")
        videos = extractor.extract_video_metadata(
            channel_id=CHANNEL_ID if CHANNEL_ID != "YOUR_CHANNEL_ID_HERE" else None,
            username=USERNAME,
            max_results=MAX_RESULTS
        )
        
        if videos:
            print(f"✅ Extracted {len(videos)} videos")
            
            # Save to CSV
            filename = extractor.save_to_csv(videos, OUTPUT_FILENAME)
            print(f"💾 Saved to: {filename}")
            
            return filename
        else:
            print("❌ No videos extracted")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def example_limited_extraction():
    """Example 2: Extract only recent videos (limited results)"""
    print("\n" + "="*60)
    print("📋 EXAMPLE 2: Limited Extraction (Recent 20 Videos)")
    print("="*60)
    
    if not validate_configuration():
        return
    
    try:
        extractor = YouTubeMetadataExtractor(api_key=YOUTUBE_API_KEY)
        
        # Extract only 20 most recent videos
        videos = extractor.extract_video_metadata(
            channel_id=CHANNEL_ID if CHANNEL_ID != "YOUR_CHANNEL_ID_HERE" else None,
            username=USERNAME,
            max_results=20
        )
        
        if videos:
            print(f"✅ Extracted {len(videos)} recent videos")
            
            # Display summary
            df = extractor.get_dataframe(videos)
            print(f"\n📊 Summary of recent videos:")
            print(f"  Total views: {df['view_count'].sum():,}")
            print(f"  Average views: {df['view_count'].mean():.0f}")
            print(f"  Most viewed: {df.loc[df['view_count'].idxmax(), 'title'][:50]}...")
            
            # Save with custom filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'recent_videos_{timestamp}.csv'
            extractor.save_to_csv(videos, filename)
            
        else:
            print("❌ No videos extracted")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_data_analysis():
    """Example 3: Extract data and perform basic analysis"""
    print("\n" + "="*60)
    print("📋 EXAMPLE 3: Data Extraction with Analysis")
    print("="*60)
    
    if not validate_configuration():
        return
    
    try:
        extractor = YouTubeMetadataExtractor(api_key=YOUTUBE_API_KEY)
        
        # Extract metadata (limit to 50 for faster analysis)
        videos = extractor.extract_video_metadata(
            channel_id=CHANNEL_ID if CHANNEL_ID != "YOUR_CHANNEL_ID_HERE" else None,
            username=USERNAME,
            max_results=50
        )
        
        if not videos:
            print("❌ No videos extracted for analysis")
            return
        
        # Convert to DataFrame for analysis
        df = extractor.get_dataframe(videos)
        
        print(f"✅ Analyzing {len(videos)} videos...")
        
        # Basic statistics
        print(f"\n📈 Channel Statistics:")
        print(f"  Total videos analyzed: {len(df)}")
        print(f"  Total views: {df['view_count'].sum():,}")
        print(f"  Total likes: {df['like_count'].sum():,}")
        print(f"  Average views per video: {df['view_count'].mean():.0f}")
        print(f"  Average likes per video: {df['like_count'].mean():.0f}")
        
        # Top performing videos
        print(f"\n🏆 Top 5 Most Viewed Videos:")
        top_videos = df.nlargest(5, 'view_count')[['title', 'view_count', 'like_count']]
        for idx, (_, video) in enumerate(top_videos.iterrows(), 1):
            title = video['title'][:40] + "..." if len(video['title']) > 40 else video['title']
            print(f"  {idx}. {title}")
            print(f"     Views: {video['view_count']:,} | Likes: {video['like_count']:,}")
        
        # Save analysis results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'video_analysis_{timestamp}.csv'
        extractor.save_to_csv(videos, filename)
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def example_channel_by_username():
    """Example 4: Extract from channel using username instead of channel ID"""
    print("\n" + "="*60)
    print("📋 EXAMPLE 4: Extract by Username")
    print("="*60)
    
    # For this example, let's use a known public username
    # You can change this to any public YouTube username
    example_username = input("Enter a YouTube username (without @): ").strip()
    
    if not example_username:
        print("❌ No username provided")
        return
    
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY_HERE":
        print("❌ API key not configured")
        return
    
    try:
        extractor = YouTubeMetadataExtractor(api_key=YOUTUBE_API_KEY)
        
        # First, get channel information
        channel_id = extractor.get_channel_id(username=example_username)
        if not channel_id:
            print(f"❌ Channel not found for username: {example_username}")
            return
        
        print(f"✅ Found channel ID: {channel_id}")
        
        # Extract limited number of videos for demo
        videos = extractor.extract_video_metadata(
            username=example_username,
            max_results=10
        )
        
        if videos:
            print(f"✅ Extracted {len(videos)} videos from @{example_username}")
            
            # Show sample data
            print(f"\n📹 Sample videos:")
            for i, video in enumerate(videos[:3], 1):
                print(f"  {i}. {video['title'][:50]}...")
                print(f"     URL: {video['url']}")
                print(f"     Views: {video['view_count']:,}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function to run examples"""
    print("🎬 YouTube Metadata Extractor - Example Usage")
    print("=" * 60)
    
    while True:
        print("\nChoose an example to run:")
        print("1. Basic metadata extraction (your channel)")
        print("2. Limited extraction (recent 20 videos)")
        print("3. Data extraction with analysis")
        print("4. Extract by username (any public channel)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            example_basic_extraction()
        elif choice == '2':
            example_limited_extraction()
        elif choice == '3':
            example_data_analysis()
        elif choice == '4':
            example_channel_by_username()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()