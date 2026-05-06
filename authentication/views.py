from django.shortcuts import render, redirect
from .models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
import logging

logger = logging.getLogger(__name__)

def setup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        pin = request.POST.get("pin")

        User.objects.all().delete()  # keep only one user
        hashed_pin = make_password(pin)
        User.objects.create(name=name, pin=hashed_pin)

        return redirect('authentication:login')

    return render(request, 'authentication/setup.html')


def login(request):
    if request.method == "POST":
        name = request.POST.get("name")
        pin = request.POST.get("pin")
        
        # Check if user exists
        try:
            user = User.objects.get(name=name)
            logger.info(f'Login attempt for known user: {user.name}')
        except User.DoesNotExist:
            logger.warning(f'Login attempt: User "{name}" not found')
            return render(request, 'authentication/login.html', {'error': 'User not found. Please check your name.'})
        
        # Check if user is locked
        if user.is_locked:
            if user.lock_time and timezone.now() > user.lock_time + timedelta(seconds=30):
                user.is_locked = False
                user.failed_attempts = 0
                user.save()
                logger.info(f'User {user.name} unlocked after timeout')
            else:
                logger.warning(f'User {user.name} is locked - redirecting to lockout')
                return redirect('lockout')
        
        # Check PIN
        if check_password(pin, user.pin):
            user.failed_attempts = 0
            user.save()
            logger.info(f'Successful login for user: {user.name}')
            return redirect('/dashboard/')  # Redirect to dashboard 

        else:
             user.failed_attempts += 1
             logger.warning(f'Failed login attempt for user {user.name} - Attempts: {user.failed_attempts}')
             if user.failed_attempts >= 3:
                user.is_locked = True
                user.lock_time = timezone.now()
                user.save()
                logger.error(f'User {user.name} locked after 3 failed attempts')
                return redirect('authentication:lockout')
             user.save()
             return render(request, 'authentication/login.html', {'error': 'Incorrect PIN. Try again.'})
    
    # Check if any user exists, if not redirect to setup
    if not User.objects.exists():
        logger.warning('Login attempt: No user found - redirecting to setup')
        return redirect('authentication:setup')
            
    return render(request, 'authentication/login.html')         
def lockout(request):
    return render(request, 'authentication/lockout.html')
