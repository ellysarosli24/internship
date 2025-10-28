from django.urls import path
from . import views
from .views import ProfileView, BlogListView, BlogDetailView, BlogCategoryView, blog_search


urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('video/', views.video_list, name='video_list'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),

    path('services/', views.service_list, name='service_list'),
    path('service/<int:service_id>/payment/', views.mock_payment, name='mock_payment'),
    path('payment/<int:service_id>/receipt/', views.payment_receipt, name='payment_receipt'),
    path('invoice/<str:transaction_id>/', views.download_invoice, name='download_invoice'),
    
    path('contactus/', views.contactus, name='contactus'),
    path('api/validate-whatsapp/', views.validate_whatsapp_number, name='validate_whatsapp'),
    
    path('profil-syarikat/', ProfileView.as_view(), name='profile'),

    path('blog/search/', views.blog_search, name='blog_search'),        # Specific
    path('blog/category/<slug:slug>/', BlogCategoryView.as_view(), name='blog_category'),  # Specific
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),  # General
    path('blog/', BlogListView.as_view(), name='blog_list'),

    path('daftar/', views.daftar_kursus_view, name='daftar_kursus'),
    
    # Halaman untuk process form submission - UBAH URL INI
    path('daftar/proses/', views.proses_daftar, name='proses_daftar'),
    
    # Halaman kejayaan selepas pendaftaran
    path('daftar/berjaya/', views.pendaftaran_berjaya, name='pendaftaran_berjaya'),

    path('export-kursus/', views.export_kursus_excel, name='export_kursus'),
]