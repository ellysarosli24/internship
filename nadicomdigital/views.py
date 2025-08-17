from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Service, Payment
from django import forms
from django.core.mail import send_mail
from django.conf import settings

def homepage(request):
    return render(request, 'homepage.html')

def video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'video.html', {'videos': videos})

def service_list(request):
    services = Service.objects.all()
    categories = Service.CATEGORY_CHOICES
    return render(request, 'service_list.html', {
        'services': services,
        'categories': categories
    })

def send_payment_confirmation(payment):
    subject = f'Pengesahan Pembayaran untuk {payment.service.name}'
    message = f'''
Terima kasih atas pembayaran anda!

Butiran Pembayaran:
Perkhidmatan: {payment.service.name}
Jumlah: RM{payment.amount}
Rujukan: #{payment.id}

Hubungi kami di {settings.DEFAULT_FROM_EMAIL} jika anda mempunyai sebarang pertanyaan.
'''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [payment.customer_email],
        fail_silently=False,
    )

def mock_payment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                service=service,
                amount=service.price,
                customer_email=form.cleaned_data['email'],
                customer_name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone'],
                is_success=True
            )
            send_payment_confirmation(payment)
            return redirect('payment_success', payment.id)
    else:
        form = PaymentForm()

    return render(request, 'services/mock_payment.html', {
        'service': service,
        'form': form
    })

def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'services/payment_success.html', {'payment': payment})

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nama Penuh')
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False, label='No Telefon')