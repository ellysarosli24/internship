# nadicomdigital/management/commands/import_youtube_videos.py
from django.core.management.base import BaseCommand
from nadicomdigital.models import Video
from nadicomdigital.youtube_service import fetch_channel_videos, fetch_video_details, auto_categorize_video

class Command(BaseCommand):
    help = 'Import all videos from YouTube channel'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--max-results',
            type=int,
            default=500,
            help='Maximum number of videos to fetch'
        )
    
    def handle(self, *args, **options):
        max_results = options['max_results']
        
        self.stdout.write(f'🚀 Fetching {max_results} videos from YouTube...')
        
        videos_data = fetch_channel_videos(max_results=max_results)
        
        if not videos_data:
            self.stdout.write(self.style.ERROR('❌ No videos fetched from YouTube'))
            return
        
        created_count = 0
        updated_count = 0
        
        # Dalam loop for video_data in videos_data:
        for video_data in videos_data:
            # Auto-detect category
            auto_category = auto_categorize_video(video_data['title'], video_data['description'])
            
            # Get additional video details
            extra_details = fetch_video_details(video_data['youtube_id'])
            
            video, created = Video.objects.get_or_create(
                youtube_id=video_data['youtube_id'],
                defaults={
                    'title': video_data['title'],
                    'description': video_data['description'],
                    'thumbnail_url': video_data['thumbnail_url'],
                    'published_at': video_data['published_at'],
                    'category': auto_category,  # ✅ AUTO-ASSIGN CATEGORY!
                    'view_count': extra_details.get('view_count', 0),
                }
            )
            
            if created:
                self.stdout.write(f"✅ CREATED [{auto_category}]: {video.title}")
                created_count += 1
            else:
                # Update existing video
                video.title = video_data['title']
                video.description = video_data['description']
                video.thumbnail_url = video_data['thumbnail_url']
                video.category = auto_category  # ✅ Auto-update category juga!
                video.save()
                self.stdout.write(f"🔄 UPDATED [{auto_category}]: {video.title}")
                updated_count += 1