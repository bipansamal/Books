"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

#setting.py files
from django.conf import settings

#for static url
from django.conf.urls.static import static



urlpatterns = [
    # path('admin/', admin.site.urls),
    path("",include('base.urls.urls')),  #can access by all user admin,user or guest(without login)
    path("user/",include('base.urls.user_urls')), #can oly access by logged in user
    path("admin/",include('base.urls.admin_urls')), #can oly access by logged in admin

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)