"""
YouTube Video Metadata Extractor

This script extracts metadata from all videos in a YouTube channel using the YouTube Data API v3.
It handles pagination to retrieve ALL videos and includes proper error handling and rate limiting.

Author: YouTube Channel Scripts
License: MIT
"""

import os
import time
import csv
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import pandas as pd
except ImportError as e:
    print(f"Missing required dependencies. Please install with: pip install -r requirements.txt")
    print(f"Error: {e}")
    exit(1)


class YouTubeMetadataExtractor:
    """
    A class to extract video metadata from YouTube channels using the YouTube Data API v3.
    """
    
    def __init__(self, api_key: str, max_retries: int = 3, retry_delay: int = 1):
        """
        Initialize the YouTube API client.
        
        Args:
            api_key (str): YouTube Data API v3 key
            max_retries (int): Maximum number of retries for API calls
            retry_delay (int): Delay between retries in seconds
        """
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.youtube = None
        self._setup_logging()
        self._build_service()
    
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('youtube_extractor.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _build_service(self):
        """Build the YouTube API service."""
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            self.logger.info("YouTube API service initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize YouTube API service: {e}")
            raise
    
    def _make_api_request(self, request_func, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Make an API request with retry logic and rate limiting.
        
        Args:
            request_func: The API request function to call
            **kwargs: Arguments to pass to the API request
            
        Returns:
            Dict containing the API response or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                response = request_func(**kwargs).execute()
                return response
            except HttpError as e:
                if e.resp.status == 403:
                    self.logger.error("API quota exceeded or invalid API key")
                    raise
                elif e.resp.status == 404:
                    self.logger.error("Channel not found")
                    raise
                elif e.resp.status in [500, 502, 503, 504]:
                    self.logger.warning(f"Server error (attempt {attempt + 1}/{self.max_retries}): {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    else:
                        raise
                else:
                    self.logger.error(f"HTTP error: {e}")
                    raise
            except Exception as e:
                self.logger.error(f"Unexpected error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise
        
        return None
    
    def get_channel_id(self, username: str = None, channel_id: str = None) -> Optional[str]:
        """
        Get channel ID from username or validate existing channel ID.
        
        Args:
            username (str): YouTube username (without @)
            channel_id (str): YouTube channel ID
            
        Returns:
            str: Channel ID if found, None otherwise
        """
        if channel_id:
            # Validate channel ID by making a simple request
            try:
                response = self._make_api_request(
                    self.youtube.channels().list,
                    part='id',
                    id=channel_id
                )
                if response and response['items']:
                    self.logger.info(f"Channel ID validated: {channel_id}")
                    return channel_id
                else:
                    self.logger.error(f"Channel ID not found: {channel_id}")
                    return None
            except Exception as e:
                self.logger.error(f"Error validating channel ID: {e}")
                return None
        
        elif username:
            # Get channel ID from username
            try:
                response = self._make_api_request(
                    self.youtube.channels().list,
                    part='id',
                    forUsername=username
                )
                if response and response['items']:
                    found_id = response['items'][0]['id']
                    self.logger.info(f"Channel ID found for username '{username}': {found_id}")
                    return found_id
                else:
                    self.logger.error(f"Channel not found for username: {username}")
                    return None
            except Exception as e:
                self.logger.error(f"Error getting channel ID for username: {e}")
                return None
        
        else:
            self.logger.error("Either username or channel_id must be provided")
            return None
    
    def get_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        """
        Get the uploads playlist ID for a channel.
        
        Args:
            channel_id (str): YouTube channel ID
            
        Returns:
            str: Uploads playlist ID if found, None otherwise
        """
        try:
            response = self._make_api_request(
                self.youtube.channels().list,
                part='contentDetails',
                id=channel_id
            )
            
            if response and response['items']:
                uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                self.logger.info(f"Uploads playlist ID: {uploads_playlist_id}")
                return uploads_playlist_id
            else:
                self.logger.error("Channel not found or no uploads playlist")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting uploads playlist ID: {e}")
            return None
    
    def extract_video_metadata(self, channel_id: str = None, username: str = None, 
                             max_results: int = None) -> List[Dict[str, Any]]:
        """
        Extract metadata from all videos in a YouTube channel.
        
        Args:
            channel_id (str): YouTube channel ID
            username (str): YouTube username (alternative to channel_id)
            max_results (int): Maximum number of videos to retrieve (None for all)
            
        Returns:
            List[Dict]: List of dictionaries containing video metadata
        """
        # Get channel ID if not provided
        if not channel_id:
            channel_id = self.get_channel_id(username=username, channel_id=channel_id)
            if not channel_id:
                return []
        
        # Get uploads playlist ID
        uploads_playlist_id = self.get_uploads_playlist_id(channel_id)
        if not uploads_playlist_id:
            return []
        
        videos_metadata = []
        next_page_token = None
        page_count = 0
        total_videos = 0
        
        self.logger.info("Starting video metadata extraction...")
        
        while True:
            page_count += 1
            self.logger.info(f"Processing page {page_count}...")
            
            try:
                # Get playlist items (videos)
                playlist_response = self._make_api_request(
                    self.youtube.playlistItems().list,
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=50,  # Maximum allowed by API
                    pageToken=next_page_token
                )
                
                if not playlist_response or not playlist_response['items']:
                    break
                
                # Extract video IDs for batch processing
                video_ids = [item['snippet']['resourceId']['videoId'] 
                           for item in playlist_response['items']]
                
                # Get detailed video information in batch
                videos_response = self._make_api_request(
                    self.youtube.videos().list,
                    part='snippet,statistics,contentDetails',
                    id=','.join(video_ids)
                )
                
                if videos_response and videos_response['items']:
                    for video in videos_response['items']:
                        try:
                            video_data = self._extract_video_data(video)
                            videos_metadata.append(video_data)
                            total_videos += 1
                            
                            # Progress update every 10 videos
                            if total_videos % 10 == 0:
                                print(f"Extracted metadata for {total_videos} videos...")
                            
                        except Exception as e:
                            self.logger.warning(f"Error processing video {video.get('id', 'unknown')}: {e}")
                            continue
                
                # Check if we've reached the maximum results
                if max_results and total_videos >= max_results:
                    videos_metadata = videos_metadata[:max_results]
                    break
                
                # Check for next page
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
                
                # Rate limiting - small delay between pages
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error processing page {page_count}: {e}")
                break
        
        self.logger.info(f"Extraction completed. Total videos processed: {len(videos_metadata)}")
        return videos_metadata
    
    def _extract_video_data(self, video: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data from a video API response.
        
        Args:
            video (Dict): Video data from YouTube API
            
        Returns:
            Dict: Cleaned video metadata
        """
        snippet = video.get('snippet', {})
        statistics = video.get('statistics', {})
        content_details = video.get('contentDetails', {})
        
        # Handle empty descriptions
        description = snippet.get('description', '').strip()
        if not description:
            description = '[No description available]'
        
        # Parse upload date
        upload_date = snippet.get('publishedAt', '')
        if upload_date:
            try:
                upload_date = datetime.fromisoformat(upload_date.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
        
        return {
            'video_id': video.get('id', ''),
            'url': f"https://www.youtube.com/watch?v={video.get('id', '')}",
            'title': snippet.get('title', '').strip(),
            'description': description,
            'upload_date': upload_date,
            'duration': content_details.get('duration', ''),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'channel_id': snippet.get('channelId', ''),
            'channel_title': snippet.get('channelTitle', ''),
            'tags': snippet.get('tags', [])
        }
    
    def save_to_csv(self, videos_data: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Save video metadata to CSV file.
        
        Args:
            videos_data (List[Dict]): List of video metadata dictionaries
            filename (str): Output filename (optional)
            
        Returns:
            str: Filename where data was saved
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'youtube_videos_metadata_{timestamp}.csv'
        
        try:
            if not videos_data:
                self.logger.warning("No video data to save")
                return filename
            
            # Convert to pandas DataFrame for better CSV handling
            df = pd.DataFrame(videos_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            
            self.logger.info(f"Data saved to {filename} ({len(videos_data)} videos)")
            print(f"✅ Data successfully saved to: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
            raise
    
    def get_dataframe(self, videos_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert video metadata to pandas DataFrame.
        
        Args:
            videos_data (List[Dict]): List of video metadata dictionaries
            
        Returns:
            pd.DataFrame: DataFrame containing video metadata
        """
        return pd.DataFrame(videos_data)


def main():
    """
    Example usage of the YouTubeMetadataExtractor class.
    """
    # Configuration - REPLACE WITH YOUR VALUES
    API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"  # Replace with your actual API key
    CHANNEL_ID = "YOUR_CHANNEL_ID_HERE"    # Replace with your channel ID
    USERNAME = None                        # Or use username instead of channel ID
    
    # Validate configuration
    if API_KEY == "YOUR_YOUTUBE_API_KEY_HERE":
        print("❌ Error: Please set your YouTube API key in the script")
        print("See README.md for instructions on obtaining an API key")
        return
    
    if CHANNEL_ID == "YOUR_CHANNEL_ID_HERE" and not USERNAME:
        print("❌ Error: Please set either CHANNEL_ID or USERNAME in the script")
        return
    
    try:
        # Initialize extractor
        print("🚀 Initializing YouTube metadata extractor...")
        extractor = YouTubeMetadataExtractor(api_key=API_KEY)
        
        # Extract video metadata
        print("📥 Extracting video metadata...")
        videos = extractor.extract_video_metadata(
            channel_id=CHANNEL_ID if CHANNEL_ID != "YOUR_CHANNEL_ID_HERE" else None,
            username=USERNAME
        )
        
        if not videos:
            print("❌ No videos found or extraction failed")
            return
        
        print(f"✅ Successfully extracted metadata for {len(videos)} videos")
        
        # Display sample data
        if videos:
            print("\n📊 Sample video data:")
            sample_video = videos[0]
            for key, value in sample_video.items():
                if key == 'description':
                    # Truncate long descriptions
                    desc = str(value)[:100] + "..." if len(str(value)) > 100 else value
                    print(f"  {key}: {desc}")
                else:
                    print(f"  {key}: {value}")
        
        # Save to CSV
        print("\n💾 Saving data to CSV...")
        csv_filename = extractor.save_to_csv(videos)
        
        # Create DataFrame for additional analysis
        df = extractor.get_dataframe(videos)
        print(f"\n📈 Data summary:")
        print(f"  Total videos: {len(df)}")
        print(f"  Total views: {df['view_count'].sum():,}")
        print(f"  Average views per video: {df['view_count'].mean():.0f}")
        print(f"  Most viewed video: {df.loc[df['view_count'].idxmax(), 'title']}")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        logging.error(f"Main execution error: {e}")


if __name__ == "__main__":
    main()