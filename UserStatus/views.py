from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from .tasks import set_status_to_inactive
from datetime import timedelta
from django.utils import timezone

# User = get_user_model()

# Create your views here.
def auth_user_with_email(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None

def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth_user_with_email(email, password)
        if user is not None:
            auth.login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            if user.is_superuser:
                return redirect('admin_dash')
            return redirect('customer')
        else:
            messages.info(request,'Invalid Credentials')
            
    return render(request,'UserStatus/index.html')

def sign_up(request):
    if request.method =="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request,'Email with this account already exists.')
                return redirect('signup')
            else:
                user = User.objects.create_user(first_name = first_name, last_name = last_name,username = email,email= email, password = password1)
                user.save()
                return redirect('index')
        else:
            messages.info(request,'Wrong Password')
            return redirect('signup')
    else:
        return render(request,'UserStatus/register.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def customer_dash(request):
    if request.method =='POST':
        status = request.POST['status']
        user = request.user
        user.status = status
        if not user.is_active_status:
            user.is_active_status = True
            user.save()
            email = user.email
            limit = timezone.now()+timedelta(minutes=1)
            set_status_to_inactive.apply_async([email],eta=limit)

        return render(request,'UserStatus/customer.html',{'is_active_status':user.is_active_status,'status':user.status})
    else:
        user = request.user
        return render(request,'UserStatus/customer.html',{'is_active_status':user.is_active_status,'status':user.status})


            

def admin_dash(request):
    all_customers = User.objects.filter(is_superuser=False)
    return render(request,'UserStatus/admin_dash.html',{'customers':all_customers})