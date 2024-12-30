from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import CustomUser
from .forms import LoginForm, RegisterForm, UpdateProfileForm


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if '@' in form.cleaned_data['email_username']:
                email = form.cleaned_data['email_username']
                password = form.cleaned_data['password']
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    username = user.username
                    user = authenticate(
                        request, username=username, password=password)
            else:
                username = form.cleaned_data['email_username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username,
                                    password=password)

            try:
                user = CustomUser.objects.get(username=username)
                if user is not None:
                    auth_login(request, user)
                    return redirect('/')
            except CustomUser.DoesNotExist:
                messages.error(
                    request, "Credenciales inválidas. Inténtalo de nuevo."
                )
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            CustomUser.objects.create_user(
                name=name,
                surname=surname,
                email=email,
                username=username,
                password=password
            )

            messages.success(
                request, "Usuario creado exitosamente. Inicia sesión."
            )
            new_user = authenticate(
                request, username=username, password=password)
            if new_user is not None:
                auth_login(request, new_user)
                return redirect('/')
            else:
                messages.error(
                    request, "Error al iniciar sesión con el nuevo usuario."
                )
                return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def edit_profile(request):
    user = get_object_or_404(CustomUser, username=request.user.username)

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form, 'user': user})


@login_required
def delete_account(request):
    user = get_object_or_404(CustomUser, username=request.user.username)
    if request.method == 'POST':
        user.delete()
        logout(request)
        return redirect('login')
    return render(request, 'delete_account.html', {'user': user})
