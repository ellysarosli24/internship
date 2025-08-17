from django.contrib import admin
from .models import Video, Service, Payment

@admin.register(Video)
class TutorialVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url', 'created_at')
    readonly_fields = ('get_youtube_id',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')  # Fields to display in the table
    list_filter = ('category',)  # Filter by category
    search_fields = ('name', 'category')  # Search functionality
    list_editable = ('price',)  # Allow editing price directly in the list view

@admin.register(Payment)  # Optional: Register Payment if you want to manage it in admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('service', 'amount', 'is_success', 'created_at', 'customer_email')
    list_filter = ('is_success', 'service__category')  # Filter by payment status or service category
    search_fields = ('customer_email', 'service__name')
