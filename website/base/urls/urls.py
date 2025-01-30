from django.urls import path
from base import views
# from base.views import forget_password 

urlpatterns = [
    path('', views.home, name='home'),
    path("price/",views.price,name="price"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forget-password/', views.forget_password, name='forget-password'),
    path('update-password/', views.update_password, name='update-password'),
    path('about/', views.about, name='about'),
]
