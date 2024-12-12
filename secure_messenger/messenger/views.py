from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from .crypto import encrypt_message, decrypt_message

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"Compte créé pour {username}!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Vous êtes connecté en tant que {username}.")
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

@login_required
def home(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    decrypted_messages = []
    for message in received_messages:
        decrypted_content = decrypt_message(message.content, 'your_secret_key')
        decrypted_messages.append({
            'sender': message.sender,
            'content': decrypted_content,
            'timestamp': message.timestamp
        })
    return render(request, 'home.html', {'messages': decrypted_messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.content = encrypt_message(message.content, 'your_secret_key')
            message.save()
            messages.success(request, "Message envoyé avec succès!")
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})