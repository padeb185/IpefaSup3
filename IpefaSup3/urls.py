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
from IpefaSup3.views import accueil, etudiant_view, educateur_view, professeur_view, login, welcome, add_student_views, \
    login_etudiant, login_professeur

urlpatterns = [
    path('', accueil, name='accueil'),

    path('etudiant/', etudiant_view, name='etudiant'),

    path('educateur/', educateur_view, name='educateur'),

    path('professeur/', professeur_view, name='professeur'),

    path("login/", login, name="login"),
    path("login.etudiant/", login_etudiant, name="login.etudiant"),
    path("login.professeur/", login_professeur, name="login.professeur"),
    path("welcome/", welcome, name="welcome"),

    path('welcome/add_student/', add_student_views, name='add_student'),

    path('admin/', admin.site.urls),
]
