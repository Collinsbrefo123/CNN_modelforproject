"""Convolutional_NN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from Convolution import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginpage, name='loginpage'),
    path('logout/', views.logoutpage, name='logout'),
    # model urls
    path('conv/', views.homeconvo, name='homeconvo'),
    path('predict/', views.predictImg, name='predictImg'),
    path('detection/', views.detection, name='detection'),
    path('model/', views.modelprediction, name='modelprediction'),
    path('notify/', views.notification, name= 'notification'),
    # google test url
    path('txn_home/', views.transmission, name='transmission'),
    path('google/', views.googlepage, name='googlepage'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
