from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    youtube_url = models.URLField()  # Changed from youtube_id to URLField
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Add this method to extract ID from URL when needed
    def get_youtube_id(self):
        from urllib.parse import urlparse, parse_qs
        url = self.youtube_url
        if 'youtu.be' in url:
            return url.split('/')[-1]
        elif 'youtube.com' in url:
            parsed = urlparse(url)
            return parse_qs(parsed.query).get('v', [''])[0]
        return None

    def __str__(self):
        return self.title
# Model untuk servis
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('ACCOUNTING', 'Perakaunan'),
        ('PAYROLL', 'Penggajian'),
        ('POS', 'Sistem POS'),
        ('EINVOICE', 'E-Invoice')
    ]
    
    name = models.CharField(max_length=100)  # Contoh: "SQL Accounting Basic"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

# Model untuk rekod payment (mock)
class Payment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_success = models.BooleanField(default=False)  # Status payment
    created_at = models.DateTimeField(auto_now_add=True)
    customer_email = models.EmailField(blank=True)  # Untuk rekod

    def __str__(self):
        return f"Payment for {self.service.name}"
