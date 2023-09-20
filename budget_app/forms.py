from django import forms
from django.core.exceptions import ValidationError

from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'category', 'description', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'amount': 'Сумма (тг.)',
            'transaction_type': 'Тип транзакции',
            'category': 'Категория',
            'description': 'Описание',
            'date': 'Дата',
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if 'A' not in title:
    #         raise ValidationError("Only notes with big A are allowed")
    #     return title