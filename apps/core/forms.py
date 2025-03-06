from django import forms
from .models import Contact  # تعديل الاستيراد هنا

class ContactForm(forms.Form):
    name = forms.CharField(
        label="الاسم",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-500 focus:border-violet-500 transition-all duration-300',
            'placeholder': 'أدخل اسمك'
        })
    )
    email = forms.EmailField(
        label="البريد الإلكتروني",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-500 focus:border-violet-500 transition-all duration-300',
            'placeholder': 'أدخل بريدك الإلكتروني'
        })
    )
    message = forms.CharField(
        label="الرسالة",
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-violet-500 focus:border-violet-500 transition-all duration-300',
            'placeholder': 'أدخل رسالتك',
            'rows': 5
        })
    )