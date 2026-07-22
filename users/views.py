from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, LoginForm, UserUpdateForm
from .token import account_activation_token

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            try:
                current_site = get_current_site(request)
                subject = 'Verify your email to activate account'
                message = render_to_string('users/email-verification.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject=subject, message=message)
            except Exception as e:
                # If email backend fails, log or fall back gracefully
                messages.warning(request, "User registered. Verification email could not be sent automatically.")
            return redirect('email-verification-sent')
    return render(request, 'users/register.html', {'form': form})

def email_verification(request, uidb64, token):
    try:
        unique_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=unique_id)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect('email-verification-success')
    else:
        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'users/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'users/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'users/email-verification-failed.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('index')

@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'user_form': user_form})