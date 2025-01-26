from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate



def home(request):
    return render(request, 'base/home.html')


def register(request):
    if request.method == "POST":
        fullname = request.POST.get("Fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("c-password")

        if password != confirm_password:
            messages.error(request, "Password does't match!")
            return redirect("register")

        if User.objects.filter(username=email).exists(): # username is form database and >>>email<< form our custom form
            messages.error(request, "email already exits")
            return redirect("register")
        
        user = User.objects.create_user(first_name=fullname,username=email, password=confirm_password)
        user.save()
        login(request,user)
        return redirect("home")
    
    return render(request, 'base/register.html')


def user_login(request):
    return render(request, 'base/login.html')

def user_logout(request):
    logout(request)
    return redirect("home")