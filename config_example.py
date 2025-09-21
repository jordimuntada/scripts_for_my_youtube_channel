"""
Configuration template for YouTube Metadata Extractor

Copy this file to 'config.py' and fill in your actual values.
Never commit config.py with real credentials to version control!
"""

# YouTube Data API v3 Configuration
# Get your API key from: https://console.developers.google.com/
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"

# Channel Configuration (use either channel_id OR username, not both)
# You can find your channel ID in YouTube Studio or by using the helper function
CHANNEL_ID = "UCxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your channel ID (starts with UC)
USERNAME = None  # Alternative: your YouTube username (without @)

# Optional: Limit the number of videos to extract (None for all videos)
MAX_RESULTS = None  # Set to a number like 100 to limit results

# Rate limiting configuration
MAX_RETRIES = 3      # Number of retries for failed API calls
RETRY_DELAY = 1      # Base delay between retries (seconds)

# Output configuration
OUTPUT_FILENAME = None  # None for auto-generated timestamp filename
INCLUDE_STATISTICS = True  # Include view counts, likes, etc.
INCLUDE_TAGS = True       # Include video tags

# Example configurations for different scenarios:

# Configuration for testing (extract only first 10 videos)
# MAX_RESULTS = 10

# Configuration for a specific channel by username
# USERNAME = "exampleusername"
# CHANNEL_ID = None

# Configuration for rate-limited extraction (slower but more reliable)
# MAX_RETRIES = 5
# RETRY_DELAY = 2