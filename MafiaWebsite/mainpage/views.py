from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def home(request):
    return render(request, 'mainpage/home.html')


def register(request):
    return render(request, 'mainpage/register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        error_messages = []

        if User.objects.filter(username=username).exists():
            error_messages.append('This username is already taken. Please choose another username.')

        if User.objects.filter(email=email).exists():
            error_messages.append('There is already an account with this email.')

        if password != password2:
            error_messages.append("The password didn't match, please enter a valid password.")

        if error_messages:
            return render(request, 'mainpage/register.html', {'error_messages': error_messages})

        user = User.objects.create_user(username=username, email=email, password=password)
        # Pārējais reģistrācijas kods
        
        return redirect('home')  # Pāreja uz pieteikšanās lapu

    return render(request, 'mainpage/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Veikt nepieciešamos pasākumus, lai pārsūtītu lietotāju uz profilu
            return redirect('home')  # Aizvietojiet 'profile' ar sava profila ceļu
        else:
            # Apstrādājiet nepareizu lietotājvārdu un/vai paroli
            return render(request, 'mainpage/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'mainpage/login.html')
    
    
