from django.shortcuts import render
from .models import Member
from functools import wraps

from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

def index(request):
    members = Member.objects.all()
    query = request.GET.get('q', '')
    if query:
        members = members.filter(
            firstName__icontains=query
        ) | members.filter(
            lastName__icontains=query
        ) | members.filter(
            id__icontains=query
        ) | members.filter(
            country__icontains=query
        )
    return render(request, 'index.html', {
        'members': members,
        'query': query,
        'total': members.count()
    })

def profile(request, id):
    member = Member.objects.get(id=id)
    return render(request, 'profile.html', {'member': member})

INPUT_CLASS = (
    'w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 '
    'text-sm text-white focus:outline-none focus:border-brand-500'
)


# ---------- Forms ----------
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': INPUT_CLASS, 'placeholder': 'Username', 'autofocus': True})
        self.fields['password'].widget.attrs.update(
            {'class': INPUT_CLASS, 'placeholder': 'Password'})


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {'username': 'Username', 'email': 'Email',
                        'password1': 'Password', 'password2': 'Confirm password'}
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': INPUT_CLASS, 'placeholder': placeholders.get(name, '')})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = False        # new accounts are always normal users
        user.is_superuser = False
        if commit:
            user.save()
        return user


# ---------- Admin / User permissions ----------
def admin_required(view_func):
    """Admin = is_staff or is_superuser. Normal users are redirected with a message."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to do that (Admin only).')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ---------- Authentication views ----------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form, 'next': request.GET.get('next', '')})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')