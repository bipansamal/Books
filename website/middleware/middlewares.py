from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Only process if the request is to the dashboard
        if request.path.startswith('/user/') or request.path.startswith('/admin/'):
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if not authenticated
            
            if request.path.startswith('/admin/'):
                if request.user.is_staff==0 and request.user.is_superuser==0: 
                    return redirect(reverse('user-dashboard'))  #redirect to user dashboard beacuse user doesnot have access to open admin dashb oard
                
            if request.path.startswith('/user/'):
                if request.user.is_staff==1 or request.user.is_superuser==1: 
                    return redirect(reverse('dashboard'))   #redirect to admin dashboard beacuse admin doesnot have access to open user dashb oard
                
        # Continue with the request processing pipeline
        response = self.get_response(request)
        return response

# class UserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
        
#     def __call__(self, request):
#         # Only process if the request is to the dashboard
#         if request.path.startswith('/user/') or request.path.startswith('/admin/'):
#             # Check if the user is authenticated
#             if not request.user.is_authenticated:
#                 return redirect('login')  # Redirect to login if not authenticated
            
#             if request.user.is_staff==0 and request.user.is_superuser==0: 
#                 return redirect(reverse('user-dashboard')) 
            
#         # Continue with the request processing pipeline
#         response = self.get_response(request)
#         return response

# class AdminMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
        
#     def __call__(self, request):
#         # Only process if the request is to the dashboard
#         if request.path.startswith('/admin/'):
#             # Check if the user is authenticated
#             if not request.user.is_authenticated:
#                 return redirect('login')  # Redirect to login if not authenticated
        
#         if request.user.is_staff==1 and request.user.is_superuser==1: 
#             return redirect(reverse('dashboard')) 
        
#         response = self.get_response(request)
#         return response
