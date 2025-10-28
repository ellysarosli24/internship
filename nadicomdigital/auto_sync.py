# nadicomdigital/auto_sync.py
from django.utils import timezone
from datetime import timedelta
from .models import Video
from .youtube_service import fetch_channel_videos, fetch_video_details, auto_categorize_video
import logging

logger = logging.getLogger(__name__)

def auto_sync_new_videos():
    """
    Automatically sync new videos from YouTube
    Runs in background when users access the website
    """
    try:
        # Check last sync time (jangan run terlalu kerap)
        last_sync = getattr(auto_sync_new_videos, '_last_sync', None)
        now = timezone.now()
        
        # Only sync once every 30 minutes untuk avoid API quota
        if last_sync and (now - last_sync).total_seconds() < 1800:  # 30 minutes
            return "sync_skipped_too_soon"
        
        logger.info("🔄 Auto-syncing new videos from YouTube...")
        
        # Fetch latest videos (limit to 10 untuk jimat quota)
        videos_data = fetch_channel_videos(max_results=10)
        
        if not videos_data:
            return "no_videos_fetched"
        
        new_count = 0
        for video_data in videos_data:
            # Check if video already exists
            if not Video.objects.filter(youtube_id=video_data['youtube_id']).exists():
                # Auto-categorize
                auto_category = auto_categorize_video(video_data['title'], video_data['description'])
                extra_details = fetch_video_details(video_data['youtube_id'])
                
                # Create new video
                Video.objects.create(
                    youtube_id=video_data['youtube_id'],
                    title=video_data['title'],
                    description=video_data['description'],
                    thumbnail_url=video_data['thumbnail_url'],
                    published_at=video_data['published_at'],
                    category=auto_category,
                    view_count=extra_details.get('view_count', 0),
                )
                new_count += 1
                logger.info(f"✅ Auto-added: {video_data['title']}")
        
        # Update last sync time
        auto_sync_new_videos._last_sync = now
        
        if new_count > 0:
            logger.info(f"🎉 Auto-sync complete! {new_count} new videos added.")
            return f"sync_success_{new_count}_added"
        else:
            logger.info("ℹ️  Auto-sync: No new videos found.")
            return "sync_no_new_videos"
            
    except Exception as e:
        logger.error(f"❌ Auto-sync failed: {e}")
        return "sync_failed"