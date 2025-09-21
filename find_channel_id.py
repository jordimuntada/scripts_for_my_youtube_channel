#!/usr/bin/env python3
"""
Helper script to find YouTube channel ID from username or URL.

This utility helps you find your channel ID when you only know your username.
"""

import sys
import re

def find_channel_id_from_api(username: str, api_key: str) -> str:
    """
    Find channel ID using YouTube Data API v3.
    
    Args:
        username (str): YouTube username (without @)
        api_key (str): YouTube Data API key
        
    Returns:
        str: Channel ID if found
    """
    try:
        from googleapiclient.discovery import build
        
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        response = youtube.channels().list(
            part='id',
            forUsername=username
        ).execute()
        
        if response['items']:
            return response['items'][0]['id']
        else:
            return None
            
    except ImportError:
        print("❌ Error: google-api-python-client not installed")
        print("Install with: pip install -r requirements.txt")
        return None
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None


def extract_channel_id_from_url(url: str) -> str:
    """
    Extract channel ID from various YouTube URL formats.
    
    Args:
        url (str): YouTube channel URL
        
    Returns:
        str: Channel ID if found in URL
    """
    # Pattern for channel ID (UC followed by 22 characters)
    channel_id_pattern = r'UC[a-zA-Z0-9_-]{22}'
    
    # Common URL patterns
    patterns = [
        r'youtube\.com/channel/(UC[a-zA-Z0-9_-]{22})',
        r'youtube\.com/c/([^/?]+)',
        r'youtube\.com/user/([^/?]+)',
        r'youtube\.com/@([^/?]+)',
    ]
    
    # First check if there's already a channel ID in the URL
    channel_id_match = re.search(channel_id_pattern, url)
    if channel_id_match:
        return channel_id_match.group(0)
    
    # Extract username from various URL formats
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def main():
    """Main function to run the channel ID finder."""
    print("🔍 YouTube Channel ID Finder")
    print("=" * 50)
    
    print("\nThis tool helps you find your YouTube channel ID.")
    print("You can provide either:")
    print("1. Your YouTube username")
    print("2. Your YouTube channel URL")
    print("3. Use the API to look up by username")
    
    while True:
        print("\nChoose an option:")
        print("1. Extract from YouTube URL")
        print("2. Look up by username (requires API key)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\n" + "-" * 40)
            print("EXTRACT FROM URL")
            print("-" * 40)
            
            url = input("Enter your YouTube channel URL: ").strip()
            if not url:
                print("❌ No URL provided")
                continue
            
            result = extract_channel_id_from_url(url)
            if result:
                if result.startswith('UC'):
                    print(f"✅ Channel ID found: {result}")
                else:
                    print(f"✅ Username found: {result}")
                    print("Note: You can use this username in the script, or use option 2 to get the actual channel ID")
            else:
                print("❌ Could not extract channel ID or username from URL")
                print("Make sure you're using a valid YouTube channel URL")
        
        elif choice == '2':
            print("\n" + "-" * 40)
            print("LOOK UP BY USERNAME")
            print("-" * 40)
            
            api_key = input("Enter your YouTube Data API key: ").strip()
            if not api_key:
                print("❌ No API key provided")
                continue
            
            username = input("Enter YouTube username (without @): ").strip()
            if not username:
                print("❌ No username provided")
                continue
            
            print("🔍 Looking up channel ID...")
            channel_id = find_channel_id_from_api(username, api_key)
            
            if channel_id:
                print(f"✅ Channel ID found: {channel_id}")
                print(f"Username: {username}")
                print("\nYou can use either in your configuration:")
                print(f"CHANNEL_ID = '{channel_id}'")
                print(f"# OR")
                print(f"USERNAME = '{username}'")
            else:
                print("❌ Channel not found")
                print("Make sure:")
                print("- The username is correct")
                print("- The channel is public")
                print("- Your API key is valid")
        
        elif choice == '3':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-3.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()