from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView, 
    LogoutView,
    PasswordChangeView,
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from datetime import datetime

from .forms import EmailChangeForm

class HomeView(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'today': datetime.today()}


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'home/register.html'
    success_url = reverse_lazy('home')

    # override the method to login right after successfull registration
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
    
    # override the method to redirect the user to home page
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    

class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/authorized.html'
    login_url = '/admin'


class ProfileView(LoginRequiredMixin, TemplateView):
    context_object_name = "profile"
    template_name = "home/profile.html"
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_name'] = self.request.user.get_username

        return context
    
class ChangeEmailView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EmailChangeForm
    template_name = "home/change_email.html"
    success_url = "/profile"

    def get_object(self):
        return self.request.user
    

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'home/change_password.html'
    success_url = "/profile"

class MyPasswordResetView(PasswordResetView):
    template_name = 'home/password_reset.html'

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'home/password_reset_done.html'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'home/password_reset_confirm.html'

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'home/password_reset_complete.html'

