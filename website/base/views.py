from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode


from . models import About



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

    if request.user.is_authenticated:
        return redirect("home")          
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("Email:", email)
        print("Password:", password)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff == 1:
                return redirect('dashboard')
            return redirect('home')
        else:
            messages.error(request, "Username or password does not match")
            return redirect('login')

    return render(request, 'base/login.html')

def dashboard(request):
    if request.method == "POST":
        description = request.POST.get("description")
        status  = request.POST.get("status")
        about = About.objects.create(description=description,status=status)
        about.save()
        return redirect("dashboard")

    return render(request,"base/admin/dashboard.html")

def user_logout(request):
    logout(request)
    return redirect("home")



def about(request):
    about = About.objects.get(status = 1)
    return render(request, 'base/about.html', {"about":about})


def details(request):
    about = About.objects.get(status = 1)
    return render(request, 'base/admin/detail.html', {"about":about})

def forget_password(request):
    if request.method =='POST':
        email = request.POST.get('email') 
        subject = "Password Recovery Email"

        # Define the context for dynamic content
        user = User.objects.get(username = email)
        if user is not None:
            context = {
                'name': user.get_full_name,
                'company': settings.APP_NAME,
                'email': user.username,
                'update_password' : settings.APP_URL + reverse('update-password') + '?' + urlencode({'receiver': email })
            }

            # Render the HTML template with context
            message = render_to_string('base/email_template.html', context)

            from_email = settings.EMAIL_HOST_USER
            receiver = [email]
            
            #send the mail to the user
            send_mail(subject, message, from_email, receiver, html_message=message)
            
            messages.success(request, 'Email Send Successfully')
            return redirect('login')
        else:
            messages.error(request,'User Doenot exists in our database')
            return redirect('forget.password')
    return render(request,'base/forget_password.html')

def update_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        newpassword=request.POST.get('password')
        conformpassowrd=request.POST.get('cpassword')

        if newpassword == conformpassowrd:
            user = User.objects.get(username=email)
            if user is not None:
                user.set_password(newpassword)
                user.save()
                messages.success(request,"Password changed successfully",)
                return redirect("home")
        else:
            messages.error(request, "New password did not match the confirm password")
            return redirect("update-password")
    receiver = request.GET.get('receiver')
    return render(request,'base/new_password.html',{'email':receiver})
    