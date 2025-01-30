from django.urls import path
from base import views
# from base.views import forget_password 

urlpatterns = [
    path("user-dashboard/",views.userDashboard,name="user-dashboard")
]
