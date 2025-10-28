from django import forms
from .models import Peserta

class PendaftaranForm(forms.ModelForm):
    class Meta:
        model = Peserta
        fields = ['nama', 'no_ic', 'syarikat', 'no_telefon', 'email']
        widgets = {
            'nama': forms.TextInput(attrs={'placeholder': 'Nama Penuh'}),
            'no_ic': forms.TextInput(attrs={'placeholder': 'Contoh: 901231-01-1234'}),
            'syarikat': forms.TextInput(attrs={'placeholder': 'Nama Syarikat'}),
            'no_telefon': forms.TextInput(attrs={'placeholder': 'Contoh: 012-345 6789'}),
            'email': forms.EmailInput(attrs={'placeholder': 'alamat@email.com'}),
        }
    
    def clean_no_ic(self):
        no_ic = self.cleaned_data['no_ic']
        # Basic validation untuk format IC
        if len(no_ic) not in [12, 14]:
            raise forms.ValidationError("Sila masukkan nombor IC yang valid (12 atau 14 digit)")
        return no_ic
    
    def clean_no_telefon(self):
        no_telefon = self.cleaned_data['no_telefon']
        # Basic validation untuk nombor telefon Malaysia
        if not no_telefon.startswith(('+60', '0')):
            raise forms.ValidationError("Sila masukkan nombor telefon Malaysia yang valid")
        return no_telefon