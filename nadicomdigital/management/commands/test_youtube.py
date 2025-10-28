from django.core.management.base import BaseCommand
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Test YouTube API connection'
    
    def handle(self, *args, **options):
        print("🧪 Testing YouTube API...")
        
        url = f"https://www.googleapis.com/youtube/v3/search?key={settings.YOUTUBE_API_KEY}&channelId={settings.YOUTUBE_CHANNEL_ID}&part=snippet&maxResults=1"
        
        # Add headers to simulate web request
        headers = {
            'Referer': 'http://localhost:8000',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS("✅ API Working!"))
            data = response.json()
            if data.get('items'):
                self.stdout.write(f"🎥 Video: {data['items'][0]['snippet']['title']}")
            else:
                self.stdout.write("ℹ️ No videos found")
        else:
            self.stdout.write(self.style.ERROR("❌ API Failed"))
            print(response.json())