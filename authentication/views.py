from django.shortcuts import render, redirect
from .models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password

def setup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        pin = request.POST.get("pin")

        User.objects.all().delete()  # keep only one user
        hashed_pin = make_password(pin)
        User.objects.create(name=name, pin=hashed_pin)

        return redirect('login')

    return render(request, 'authentication/setup.html')


def login(request):
    user = User.objects.first()

    if not user:
        return redirect('setup')
    
    if user.is_locked:
        if user.lock_time and timezone.now() > user.lock_time + timedelta(seconds=30):
            user.is_locked = False
            user.failed_attempts = 0
            user.save()
        else:
            return redirect('lockout')

    if request.method == "POST":
        pin = request.POST.get("pin")

        if check_password(pin, user.pin):
            user.failed_attempts = 0
            user.save()
            return redirect('setup')  # MAFROOD A DIRECT LEL DASHBOARD BTA3T HALA 

        else:
             user.failed_attempts += 1
             if user.failed_attempts >= 3:
                user.is_locked = True
                user.lock_time = timezone.now()
                user.save()
                return redirect('lockout')
             user.save()
             return render(request, 'authentication/login.html', {'error': 'Incorrect PIN. Try again.'})
            
    return render(request, 'authentication/login.html')         
def lockout(request):
    return render(request, 'authentication/lockout.html')
