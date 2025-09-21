# YouTube Video Metadata Extractor

A Python script that extracts metadata from all videos in a YouTube channel using the YouTube Data API v3. This tool handles pagination to retrieve ALL videos and includes proper error handling, rate limiting, and progress tracking.

## 🚀 Features

- **Complete Video Extraction**: Retrieves all publicly visible videos from any YouTube channel
- **Comprehensive Metadata**: Extracts video ID, URL, title, description, upload date, view counts, likes, and more
- **Pagination Handling**: Automatically handles API pagination to get ALL videos (not just the first 50)
- **Error Handling & Rate Limiting**: Robust error handling with exponential backoff and retry logic
- **Multiple Output Formats**: Save to CSV or work with pandas DataFrame
- **Progress Tracking**: Real-time progress updates during extraction
- **Flexible Input**: Works with channel ID or username
- **Modular Design**: Reusable class for different channels and use cases

## 📋 Extracted Data Fields

For each video, the following metadata is extracted:

| Field | Description |
|-------|-------------|
| `video_id` | Unique YouTube video identifier |
| `url` | Full YouTube video URL |
| `title` | Video title |
| `description` | Video description (handles empty descriptions) |
| `upload_date` | Video upload date and time |
| `duration` | Video duration |
| `view_count` | Number of views |
| `like_count` | Number of likes |
| `comment_count` | Number of comments |
| `channel_id` | Channel identifier |
| `channel_title` | Channel name |
| `tags` | Video tags/keywords |

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jordimuntada/scripts_for_my_youtube_channel.git
cd scripts_for_my_youtube_channel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `google-api-python-client` - YouTube Data API client
- `pandas` - Data manipulation and CSV export
- `google-auth` - Authentication for Google APIs

### 3. Get YouTube Data API Credentials

#### Step-by-Step Guide:

1. **Go to Google Cloud Console**: Visit [Google Cloud Console](https://console.cloud.google.com/)

2. **Create or Select a Project**:
   - Create a new project or select an existing one
   - Note your project name for reference

3. **Enable YouTube Data API v3**:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click on it and press "Enable"

4. **Create API Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key
   - (Optional) Restrict the API key to YouTube Data API v3 for security

5. **Set Usage Quotas** (Important):
   - YouTube Data API has daily quotas (10,000 units per day by default)
   - Each video costs ~4-5 quota units
   - You can extract ~2000-2500 videos per day with default quota

### 4. Configuration

#### Option A: Using Configuration File (Recommended)

1. Copy the example configuration:
```bash
cp config_example.py config.py
```

2. Edit `config.py` with your values:
```python
YOUTUBE_API_KEY = "your_actual_api_key_here"
CHANNEL_ID = "UCxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your channel ID
# OR
USERNAME = "your_youtube_username"  # Alternative to channel ID
```

#### Option B: Direct Script Modification

Edit the variables directly in `youtube_metadata_extractor.py` or `example_usage.py`:

```python
API_KEY = "your_actual_api_key_here"
CHANNEL_ID = "your_channel_id_here"
```

### 5. Find Your Channel ID

If you don't know your channel ID, you can find it by:

**Method 1: YouTube Studio**
- Go to [YouTube Studio](https://studio.youtube.com/)
- Your channel ID is in the URL: `https://studio.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxxxxxx`

**Method 2: Using the Script**
```python
from youtube_metadata_extractor import YouTubeMetadataExtractor

extractor = YouTubeMetadataExtractor(api_key="your_api_key")
channel_id = extractor.get_channel_id(username="your_username")
print(f"Your channel ID: {channel_id}")
```

## 🎯 Usage

### Basic Usage

```python
from youtube_metadata_extractor import YouTubeMetadataExtractor

# Initialize extractor
extractor = YouTubeMetadataExtractor(api_key="your_api_key")

# Extract all videos from a channel
videos = extractor.extract_video_metadata(channel_id="your_channel_id")

# Save to CSV
extractor.save_to_csv(videos, "my_videos.csv")

# Or work with pandas DataFrame
df = extractor.get_dataframe(videos)
print(df.head())
```

### Command Line Usage

Run the main script:
```bash
python youtube_metadata_extractor.py
```

Or run the interactive example:
```bash
python example_usage.py
```

### Advanced Usage Examples

#### 1. Extract Limited Number of Videos
```python
# Extract only the 50 most recent videos
videos = extractor.extract_video_metadata(
    channel_id="your_channel_id",
    max_results=50
)
```

#### 2. Extract by Username
```python
# Use username instead of channel ID
videos = extractor.extract_video_metadata(username="your_username")
```

#### 3. Custom Error Handling
```python
# Initialize with custom retry settings
extractor = YouTubeMetadataExtractor(
    api_key="your_api_key",
    max_retries=5,
    retry_delay=2
)
```

#### 4. Data Analysis Example
```python
import pandas as pd

# Extract and analyze
videos = extractor.extract_video_metadata(channel_id="your_channel_id")
df = extractor.get_dataframe(videos)

# Basic statistics
print(f"Total videos: {len(df)}")
print(f"Total views: {df['view_count'].sum():,}")
print(f"Average views per video: {df['view_count'].mean():.0f}")

# Top 10 most viewed videos
top_videos = df.nlargest(10, 'view_count')[['title', 'view_count', 'upload_date']]
print(top_videos)
```

## 📁 File Structure

```
scripts_for_my_youtube_channel/
├── youtube_metadata_extractor.py    # Main extractor class
├── example_usage.py                 # Interactive examples
├── config_example.py               # Configuration template
├── requirements.txt                # Python dependencies
├── README.md                      # This file
└── config.py                     # Your configuration (create this)
```

## ⚠️ Important Notes

### API Quotas and Limits

- **Daily Quota**: 10,000 units per day (default)
- **Cost per Video**: ~4-5 quota units
- **Estimated Capacity**: ~2000-2500 videos per day
- **Reset Time**: Quotas reset at midnight Pacific Time

### Rate Limiting

The script includes built-in rate limiting:
- Exponential backoff for errors
- Small delays between API calls
- Automatic retry on temporary failures

### Data Considerations

- **Empty Descriptions**: Handled gracefully with placeholder text
- **Private Videos**: Only public videos are extracted
- **Deleted Videos**: Not included in results
- **Large Channels**: May take several minutes to complete

## 🔧 Troubleshooting

### Common Issues

**1. "API quota exceeded"**
- Wait for quota to reset (midnight PT)
- Reduce `max_results` parameter
- Request quota increase from Google

**2. "Channel not found"**
- Verify channel ID or username
- Check if channel is public
- Ensure API key has correct permissions

**3. "Invalid API key"**
- Verify API key is correct
- Check if YouTube Data API v3 is enabled
- Ensure API key restrictions allow your IP

**4. "Import errors"**
- Run `pip install -r requirements.txt`
- Check Python version (3.7+ recommended)

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Output Examples

### CSV Output Structure
```csv
video_id,url,title,description,upload_date,view_count,like_count,...
dQw4w9WgXcQ,https://www.youtube.com/watch?v=dQw4w9WgXcQ,Rick Astley - Never Gonna Give You Up,The official video for...,2009-10-25 07:57:33,1000000,50000,...
```

### DataFrame Output
```python
     video_id                                    url                    title  view_count
0  dQw4w9WgXcQ  https://www.youtube.com/watch?v=dQw4w9WgXcQ  Rick Astley - Never...     1000000
1  xyz123abc   https://www.youtube.com/watch?v=xyz123abc   Another Video Title     500000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for the YouTube Data API v3
- Python community for excellent libraries
- YouTube creators for making content to analyze!

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

---

**Happy extracting! 🎬📊**