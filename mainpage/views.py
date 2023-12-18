from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
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
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMessage, send_mail


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        # Ja lietotājs ir pieslēdzies, redirektē uz menu lapu
        return redirect('menu')
    else:
        # Ja lietotājs nav pieslēdzies, renderē sakumlapu
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
            error_messages.append(
                'This username is already taken. Please choose another username.')

        if User.objects.filter(email=email).exists():
            error_messages.append(
                'There is already an account with this email.')

        if password != password2:
            error_messages.append(
                "The password didn't match, please enter a valid password.")

        if error_messages:
            return render(request, 'mainpage/register.html', {'error_messages': error_messages})

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Saglabā informāciju par e-pasta apstiprinājumu
        profile = Profile.objects.create(
            user=user, verification_sent_at=timezone.now())
        # Parbauda vai ir neaktivu profilu 30min un ja ir tad izdzes
        call_command('delete_unverified_profiles')
        # Sūta e-pasta verifikācijas linku uz lietotāja e-pastu
        current_site = get_current_site(request)

        context = {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }
        message = render_to_string(
            'mainpage/activation_email.html', context=context)

        email = EmailMessage(
            'Activate your account',
            message,
            'team@mafiawebsite.xyz',
            [email],
        )

        email.content_subtype = 'html'
        email.send()

        successful_messages.append(
            'Please check your email for the confirmation link. If you haven\'t received the email, please also check your spam folder. If you still haven\'t received it, you can request a new confirmation email by visiting the Resend Confirmation page.')
        # Pāreja uz pieteikšanās lapu
        return render(request, 'mainpage/login.html', {'successful_messages': successful_messages})

    return render(request, 'mainpage/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Atrodi vai izveido lietotāja profilu
        profile, created = Profile.objects.get_or_create(user=user)

        # Izdzēs profilu, ja tas eksistē
        if not created:
            profile.delete()

        return render(request, 'mainpage/activate_success.html')
    else:
        return render(request, 'mainpage/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'mainpage/login.html', {'error_message': error_message})
    else:
        return render(request, 'mainpage/login.html')


def forgot_password(request):
    error_messages = []
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_messages.append('The email address does not exist.')
            return render(request, 'forgetpassword/forgot_password.html', {'error_messages': error_messages})

        if user is not None:
            # Generate password reset token and link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                f'/reset_password/{uid}/{token}/')

            # Render the HTML email template
            html_message = render_to_string('forgetpassword/password_reset_email.html', {
                'reset_link': reset_link,
                'username': user.username
            })

            # Strip HTML tags from the message
            plain_message = strip_tags(html_message)

            # Send password reset email
            subject = 'Password Reset Request'
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [
                      email], html_message=html_message)

        return render(request, 'forgetpassword/password_reset_sent.html')

    return render(request, 'forgetpassword/forgot_password.html')


def reset_password(request, uidb64, token):
    error_messages = []
    success_message = ""

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Process the password reset form
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            if password1 and password2:
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    success_message = "Your password has been successfully changed. Please login with your new password."
                    return render(request, 'mainpage/login.html', {'success_message': success_message})
                else:
                    error_messages.append(
                        "The passwords you entered do not match.")
            else:
                error_messages.append("Please enter a valid password.")
        else:
            return render(request, 'forgetpassword/reset_password.html', {'error_messages': error_messages})

    return render(request, 'forgetpassword/reset_password.html', {
        'error_messages': error_messages,
    })

def handler404(request, exception):
    return render(request, 'error.html', {'code': 404, 'message': 'Not Found'}, status=404)

def handler500(request):
    return render(request, 'error.html', {'code': 500, 'message': 'Internal Server Error'}, status=500)