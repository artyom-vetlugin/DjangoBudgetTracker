from django import forms
from django.contrib.auth.models import User

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

        widgets = {
            'email': forms.TextInput(attrs={'type':'email', 'class': 'form-control d-flex'}),
        }

        # labels = {
        #     'email': 'Адрес почты',
        # }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email уже существует')
        return email


    