from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
# Create your views here.

def cadastro(request):
    if request.method == "GET":
        return render(request, 'usuarios/cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request. POST.get('senha')
        user = User.objects.filter(username=username).exists()
        if user:
            return HttpResponse("Já existe um usuário com esse username")
       
        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )
        login_django(request, user) # loga o usuário após o cadastro
        return redirect("home")

    
def login(request):
    if request.method == "GET":
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(
            username=username,
            password=senha
        )
        if user:
            login_django(request, user)
            return redirect("home")
        else:
            return HttpResponse('Usuário ou senha inválidos')

def logout_view(request):
    logout_django(request)
    return redirect('home')
