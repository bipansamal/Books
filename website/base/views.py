from django.shortcuts import render ,redirect
import os
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password



from . models import About, Profile



def home(request):
    return render(request, 'base/home.html')

def price(request):
    return render(request, 'base/price.html')

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
        messages.success(request,"successfully submited")
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

@login_required(login_url='login')
def dashboard(request):
    users = User.objects.all()
    return render(request,"base/admin/dashboard.html",{'users':users})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect("home")



def about(request):
    about = About.objects.get(status = 1)
    return render(request, 'base/about.html', {"about":about})

@login_required(login_url='login')
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
            return redirect('forget-password')
    return render(request,'base/forget_password.html')


# def forget_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         subject = "Password Recovery Email"

#         # Check if the user exists
#         user = User.objects.filter(username=email).first()  # Avoids exception

#         if user:  # If user exists
#             context = {
#                 'name': user.get_full_name(),
#                 'company': settings.APP_NAME,
#                 'email': user.username,
#                 'update_password': settings.APP_URL + reverse('update-password') + '?' + urlencode({'receiver': email})
#             }

#             # Render the HTML template with context
#             message = render_to_string('base/email_template.html', context)

#             from_email = settings.EMAIL_HOST_USER
#             receiver = [email]

#             # Send the mail to the user
#             send_mail(subject, message, from_email, receiver, html_message=message)

#             messages.success(request, 'Email Sent Successfully')
#             return redirect('login')
#         else:  # If user does not exist
#             messages.error(request, 'User does not exist in our database')
#             return redirect('forget-password')  # Fix route name typo

#     return render(request, 'base/forget_password.html')

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



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        # profile = request.POST.get('profile')
        user = request.user
        
        oldpassword=request.POST.get('password')
        newpassword=request.POST.get('password1')
        conformpassowrd=request.POST.get('c-password')

        if check_password(oldpassword, request.user.password):
            if newpassword == conformpassowrd:
                request.user.set_password(newpassword)
                request.user.save()
                messages.success(request,"Password changed successfully",)
                return redirect("home")
            else:
                messages.error(request, "New password did not match the confirm password")
                return redirect("change-password")
        else:
            messages.error(request, "Password did not match")
            return redirect("change-password")
                  
    return render(request,'base/change_password.html')
    
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        position = request.POST.get('position')
        role = request.POST.get('role')
        image = request.FILES.get('image')

        if image:
            image_directory = os.path.join(settings.MEDIA_ROOT, "images")

            # Ensure the directory exists
            if not os.path.exists(image_directory):
                os.makedirs(image_directory)

            image_path = os.path.join(image_directory, image.name)
            
            # Save the file manually
            with open(image_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            profile = Profile(title=title, position=position, role=role, user_id=request.user.id, image=f"images/{image.name}")
            profile.save()

        messages.success(request,'Profile created Successfully')
        return redirect('profile')
    return render(request,'base/admin/profile.html')
    

def userDashboard(request):
    return render(request, 'base/user/user_dashboard.html')