from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from mainpage.models import Profile
from django.utils import timezone
from django.core.management import call_command

# Create your views here.

def home(request):
    return render(request, 'mainpage/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        error_messages = []
        successful_messages = []

        if User.objects.filter(username=username).exists():
            error_messages.append('This username is already taken. Please choose another username.')

        if User.objects.filter(email=email).exists():
            error_messages.append('There is already an account with this email.')

        if password != password2:
            error_messages.append("The password didn't match, please enter a valid password.")

        if error_messages:
            return render(request, 'mainpage/register.html', {'error_messages': error_messages})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Saglabā informāciju par e-pasta apstiprinājumu
        profile = Profile.objects.create(user=user, verification_sent_at=timezone.now())
        #Parbauda vai ir neaktivu profilu 30min un ja ir tad izdzes
        call_command('delete_unverified_profiles')
        # Sūta e-pasta verifikācijas linku uz lietotāja e-pastu
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('mainpage/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        send_mail(
            subject = mail_subject,
            message = message,
            recipient_list = [email],
            from_email = 'mafiagameeee@gmail.com',
        )
        successful_messages.append('Please check your email for the confirmation link. If you haven\'t received the email, please also check your spam folder. If you still haven\'t received it, you can request a new confirmation email by visiting the Resend Confirmation page.')
        return render(request, 'mainpage/login.html', {'successful_messages' : successful_messages})  # Pāreja uz pieteikšanās lapu

    return render(request, 'mainpage/register.html')

def activate(request, uidb64, token):
    error_messages = []
    successful_messages = []
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Atrodi attiecīgo lietotāja profilu
        profile = Profile.objects.get(user=user)

        # Izdzēs profilu
        profile.delete()

        successful_messages.append('Email verification successful. You can now log in.')
        return render(request, 'mainpage/login.html', {'successful_messages' : successful_messages})
    else:
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
            return render(request, 'mainpage/login.html', {'error': 'Invalid username or password. Please try again.'})
    else:
        return render(request, 'mainpage/login.html')
    
    