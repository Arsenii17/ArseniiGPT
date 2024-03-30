from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from .models import Chat

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

system_message = "Ты эмпатичный бот-психолог, готовый ответить на любые вопросы"

messages = [
        SystemMessage(
            content=system_message
        )        
    ]

chatik = GigaChat(credentials="OGRiYzNjNzctODE5My00NjJjLTg3ZmQtNGM1MDgyYjhmMzA0OmNmNmE1YTFmLTZmZmItNDBmZS05OWQ3LWZjODlhNTFhNDYzYg==", verify_ssl_certs=False)
   

def ask_openai(message):
    messages.append(HumanMessage(content=message))
    res = chatik(messages)
    messages.append(res)
    
    return res.content


def chatbot(request):
    chats = Chat.objects.filter(user=request.user.id)
    if request.method == 'POST':
        global system_message, messages
        if request.POST.get('system_message'):
            
            system_message = request.POST.get('system_message')
            Chat.objects.filter(user=request.user).delete()

            messages = [
                SystemMessage(
                    content=system_message
                )        
            ]
            
            
            return render(request, 'chatbot.html', {'chats': chats})


        if request.POST.get('message'):
            message = request.POST.get('message')
            response = ask_openai(message)
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()
            print(Chat.objects.latest('message'))
            return JsonResponse({'message': message, 'response': response})
        
    return render(request, 'chatbot.html', {'chats': chats})

def clear_history(request):
    Chat.objects.filter(user=request.user).delete()
    global messages
    messages = [
        SystemMessage(
            content="Ты эмпатичный бот-психолог, готовый ответить на любые вопросы"
        )        
    ]

    return redirect('chatbot')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Такой пользователь уже существует'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Пароли не совпадают'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
