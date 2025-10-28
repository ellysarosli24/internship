from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import re

class Video(models.Model):
    VIDEO_CATEGORIES = [
        ('SQL_ACCOUNTING', 'SQL Accounting'),
        ('E_INVOICE', 'E-Invoice'),
        ('DIGITAL_PAYMENT', 'Digital Payment'),
        ('POS_SYSTEM', 'POS System'),
        ('PAYROLL', 'Payroll System'),
        ('UNCATEGORIZED', 'Uncategorized'),  # ✅ TAMBAH INI
    ]
    
    # ✅ YOUTUBE IDENTITY (FIELD BARU)
    youtube_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    youtube_url = models.URLField(blank=True)
    
    # ✅ AUTO-FETCHED FIELDS
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    duration = models.CharField(max_length=20, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)  # ✅ NULLABLE DULU
    
    # ✅ BUSINESS LOGIC (FIELD LAMA YANG KEKAL)
    category = models.CharField(
        max_length=20, 
        choices=VIDEO_CATEGORIES, 
        default='UNCATEGORIZED'  # ✅ TUKE DEFAULT
    )
    view_count = models.PositiveIntegerField(default=0)  # ✅ KEKAL
    is_active = models.BooleanField(default=True)  # ✅ FIELD BARU
    
    # ✅ TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ FIELD BARU
    last_synced_at = models.DateTimeField(null=True, blank=True)  # ✅ FIELD BARU
    
    def save(self, *args, **kwargs):
        # ✅ AUTO-GENERATE YouTube URL dari ID
        if self.youtube_id and not self.youtube_url:
            self.youtube_url = f"https://youtube.com/watch?v={self.youtube_id}"
        super().save(*args, **kwargs)
    
    def get_youtube_id(self):
        return self.youtube_id  # ✅ LEBIH SIMPLE SEKARANG
    
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

class TeamMember(models.Model):
    photo = models.ImageField(upload_to='team/')
    
    class Meta:
        verbose_name = "Ahli Pasukan"
        verbose_name_plural = "Ahli Pasukan"
    
    def __str__(self):
        return f"Gambar {self.id}"
    

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tajuk")
    image = models.ImageField(upload_to='gallery/', verbose_name="Gambar")
    description = models.TextField(blank=True, verbose_name="Penerangan")
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "Gambar Galeri"
        verbose_name_plural = "Galeri"
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tajuk Gambar")
    image = models.ImageField(
        upload_to='gallery/%Y/%m/%d/',
        verbose_name="Gambar",
        help_text="Upload gambar untuk galeri"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Penerangan",
        help_text="Penerangan ringkas tentang gambar"
    )
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Tarikh Upload")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.PositiveIntegerField(default=0, verbose_name="Susunan")
    
    class Meta:
        verbose_name = "Gambar Galeri"
        verbose_name_plural = "Galeri Gambar"
        ordering = ['order', '-upload_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.title:
            self.title = f"Gallery Image {self.id}"
        super().save(*args, **kwargs)
    
    @property
    def alt_text(self):
        """Generate SEO-friendly alt text"""
        return f"{self.title} - Nadicom Digital" if self.title else "Galeri Nadicom Digital"
    

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Kategori Blog"
        verbose_name_plural = "Kategori Blog"

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tajuk Blog")
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name="Kandungan")
    excerpt = models.TextField(max_length=300, blank=True, verbose_name="Ringkasan")
    featured_image = models.ImageField(
        upload_to='blog/%Y/%m/', 
        verbose_name="Gambar Utama",
        blank=True,        # Boleh kosong dalam form
        null=True          # Boleh NULL dalam database
    )
    author = models.CharField(max_length=100, default="Admin Nadicom")
    categories = models.ManyToManyField(BlogCategory, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0, verbose_name='Jumlah Paparan')
    
    class Meta:
        verbose_name = "Post Blog"
        verbose_name_plural = "Post Blog"
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    # Optional: Auto-generate slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Kursus(models.Model):
    STATUS_KURSUS = [
        ('AKTIF', 'Aktif'),
        ('TIDAK_AKTIF', 'Tidak Aktif'),
    ]
    
    tajuk = models.CharField(max_length=200)
    tarikh = models.DateField()
    masa_mula = models.TimeField()
    masa_tamat = models.TimeField()
    lokasi = models.CharField(max_length=300)
    kapasiti = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=20, choices=STATUS_KURSUS, default='AKTIF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def slot_tersedia(self):
        peserta_count = self.peserta_set.count()
        return self.kapasiti - peserta_count
    
    def __str__(self):
        return f"{self.tajuk} - {self.tarikh}"

class Peserta(models.Model):
    nama = models.CharField(max_length=100)
    no_ic = models.CharField(max_length=20)
    syarikat = models.CharField(max_length=100)
    no_telefon = models.CharField(max_length=17)
    email = models.EmailField()
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    dihantar_pada = models.DateTimeField(auto_now_add=True)
    disahkan = models.BooleanField(default=False)
    emel_dihantar = models.BooleanField(default=False)
    tarikh_emel_dihantar = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nama} - {self.kursus.tajuk}"
    class Meta:
        # Elakkan pendaftaran duplikat untuk kursus yang sama
        unique_together = ['email', 'kursus']