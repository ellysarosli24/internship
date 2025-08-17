from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('video/', views.video_list, name='video'),
    path('services_list/', views.service_list, name='service_list'),
    path('mock-pay/<int:service_id>/', views.mock_payment, name='mock_payment'),
    path('payment-success/<int:payment_id>/', views.payment_success, name='payment_success'),
]

