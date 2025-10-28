# nadicomdigital/youtube_service.py
import requests
from django.conf import settings
from datetime import datetime

def get_channel_upload_playlist_id(channel_id):
    """Get the uploads playlist ID for a channel"""
    api_url = "https://www.googleapis.com/youtube/v3/channels"
    
    params = {
        'part': 'contentDetails',
        'id': channel_id,
        'key': settings.YOUTUBE_API_KEY
    }
    
    headers = {
        'Referer': 'http://localhost:8000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data.get('items'):
            return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return None
        
    except Exception as e:
        print(f"Error getting upload playlist: {e}")
        return None

def fetch_all_channel_videos(max_results=500):
    """Fetch ALL videos from channel using uploads playlist"""
    # Dapatkan uploads playlist ID
    uploads_playlist_id = get_channel_upload_playlist_id(settings.YOUTUBE_CHANNEL_ID)
    
    if not uploads_playlist_id:
        print("❌ Could not get uploads playlist ID")
        return []
    
    api_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    
    all_videos = []
    next_page_token = None
    
    while len(all_videos) < max_results or max_results == 0:
        params = {
            'part': 'snippet',
            'playlistId': uploads_playlist_id,
            'maxResults': min(50, max_results - len(all_videos)) if max_results > 0 else 50,
            'key': settings.YOUTUBE_API_KEY
        }
        
        if next_page_token:
            params['pageToken'] = next_page_token
        
        headers = {
            'Referer': 'http://localhost:8000',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Process videos dari playlist
            for item in data.get('items', []):
                published_at = datetime.strptime(
                    item['snippet']['publishedAt'], 
                    '%Y-%m-%dT%H:%M:%SZ'
                )
                
                video_data = {
                    'youtube_id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
                    'published_at': published_at,
                }
                all_videos.append(video_data)
            
            # Check untuk next page
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break  # No more pages
                
            # Small delay untuk avoid rate limiting
            import time
            time.sleep(0.1)
                
        except Exception as e:
            print(f"Error fetching playlist videos: {e}")
            break
    
    print(f"✅ Fetched {len(all_videos)} videos from uploads playlist")
    return all_videos

# Keep existing functions untuk auto-categorize dan details...
def auto_categorize_video(title, description):
    """Auto-detect category based on video title and description"""
    title_lower = title.lower()
    desc_lower = description.lower()
    
    category_keywords = {
        'SQL_ACCOUNTING': ['sql', 'accounting', 'akaun', 'invois', 'inventory', 'stock', 'account', 'kewangan'],
        'E_INVOICE': ['e-invoice', 'einvoice', 'e-invois', 'lhdn', 'hasil', 'tax', 'cukai'],
        'DIGITAL_PAYMENT': ['payment', 'bayaran', 'digital payment', 'ewallet', 'e-wallet', 'qr pay', 'qr code'],
        'POS_SYSTEM': ['pos', 'point of sale', 'cashier', 'cash register', 'kedai', 'retail'],
        'PAYROLL': ['payroll', 'gaji', 'salary', 'workers', 'pekerja', 'hr', 'human resource'],
    }
    
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in desc_lower:
                return category
    
    return 'UNCATEGORIZED'

def fetch_video_details(youtube_id):
    """Fetch additional details for a specific video"""
    api_url = "https://www.googleapis.com/youtube/v3/videos"
    
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': youtube_id,
        'key': settings.YOUTUBE_API_KEY
    }
    
    headers = {
        'Referer': 'http://localhost:8000',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data.get('items'):
            item = data['items'][0]
            return {
                'duration': item['contentDetails']['duration'],
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
            }
        return {}
        
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return {}

# Legacy function untuk compatibility
def fetch_channel_videos(max_results=50):
    """Legacy function"""
    return fetch_all_channel_videos(max_results)