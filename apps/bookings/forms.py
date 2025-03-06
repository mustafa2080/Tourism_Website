# bookings/forms.py
from django import forms
from .models import Booking, BankPayment
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField  # تأكد من استيراد الحقول

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package', 'special_requests', 'payment_method', 'start_date', 'number_of_people']
        widgets = {
            'package': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'date',
            }),
            'number_of_people': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            }),
        }

class BankPaymentForm(forms.ModelForm):
    # حقول بطاقة الائتمان
    card_number = CardNumberField(
        label='رقم البطاقة',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'أدخل رقم البطاقة',
            'required': True,
        })
    )
    
    expiry_date = CardExpiryField(
        label='تاريخ الانتهاء',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'MM/YY',
            'required': True,
        })
    )
    
    cvv = SecurityCodeField(
        label='CVV',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'CVV',
            'required': True,
        })
    )

    class Meta:
        model = BankPayment
        fields = [
            'bank_name',
            'account_holder',
            'transaction_date',
            'transaction_number',
            'amount',
            'receipt_image'
        ]
        widgets = {
            'bank_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'اسم البنك',
                'required': True,
            }),
            'account_holder': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'اسم صاحب الحساب',
                'required': True,
            }),
            'transaction_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'date',
                'required': True,
            }),
            'transaction_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'رقم التحويل',
                'required': True,
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'المبلغ المحول',
                'required': True,
                'min': '0',
                'step': '0.01',
            }),
            'receipt_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'accept': 'image/*',
                'required': True,
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        # التحقق من صحة المبلغ
        amount = cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('المبلغ يجب أن يكون أكبر من صفر')
        return cleaned_data
        

class BankPaymentForm(forms.ModelForm):
    card_number = CardNumberField(label='رقم البطاقة')
    expiry_date = CardExpiryField(label='تاريخ الانتهاء')
    cvv = SecurityCodeField(label='CVV')

    class Meta:
        model = BankPayment
        fields = ['bank_name', 'account_holder', 'transaction_date', 'transaction_number', 'amount', 'receipt_image']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package', 'special_requests', 'payment_method', 'start_date', 'number_of_people']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }