"""
URL configuration for IpefaSup3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import login
from django.contrib import admin
from django.urls import path
from IpefaSup3.views import login, welcome, add_student_views, welcome_teacher, welcome_administrator, welcome_student

urlpatterns = [
    path('', login, name='login'),
    path("login/", login, name="login"),
    path("welcome/", welcome, name="welcome"),
    #path('welcome_etudiant', welcome_etudiant, name='welcome_etudiant'),
    path('welcome_teacher/', welcome_teacher, name='welcome_teacher'),  # Page pour le professeur
  # Page pour l'éducateur
    path('welcome_administrator/', welcome_administrator, name='welcome_administrator'),  # Page pour l'administrateur
    path('welcome_student/', welcome_student, name='welcome_student'),  # Page
    path('welcome/add_student/', add_student_views, name='add_student'),

    path('admin/', admin.site.urls),
]
