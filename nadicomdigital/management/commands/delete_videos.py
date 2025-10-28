from django.core.management.base import BaseCommand
from nadicomdigital.models import Video

class Command(BaseCommand):
    help = 'Delete all video records for fresh start'
    
    def handle(self, *args, **options):
        count = Video.objects.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('⚠️  No videos found to delete'))
            return
            
        confirmation = input(f'⚠️  Are you sure you want to delete {count} videos? (yes/no): ')
        
        if confirmation.lower() == 'yes':
            Video.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'✅ Deleted {count} video records. Fresh start!'))
        else:
            self.stdout.write(self.style.WARNING('❌ Deletion cancelled'))