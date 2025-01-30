from django.urls import path
from base import views
# from base.views import forget_password 

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('details/', views.details, name='details'),
    path("change-password/",views.change_password,name="change-password"),
    path("profile/",views.profile,name="profile"),
]
