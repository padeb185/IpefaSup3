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
from django.urls import path
from IpefaSup3.views import (login, welcome, add_profile_views, welcome_teacher, welcome_administrator, welcome_student,
                             add_academic_ue_views, add_ue_views, student_list, edit_student,  teacher_list, edit_teacher)

urlpatterns = [
    path('', login, name='login'),
    path("login/", login, name="login"),
    path("welcome/", welcome, name="welcome"),
    #path('welcome_etudiant', welcome_etudiant, name='welcome_etudiant'),
    path('welcome_teacher/', welcome_teacher, name='welcome_teacher'),  # Page pour le professeur

    path('welcome_administrator/', welcome_administrator, name='welcome_administrator'),  # Page pour l'administrateur
    path('welcome_student/', welcome_student, name='welcome_student'),  # Page
    path('welcome_administrator/register/', add_profile_views, name='register'),
    path('welcome_administrator/add_academic_ue/', add_academic_ue_views, name='add_academic_ue'),
    path('welcome_administrator/add_ue/', add_ue_views, name='add_ue'),
    path('students/', student_list, name='student_list'),
    path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('welcome_administrator/teacher/', teacher_list, name='teacher_list'),
    path('welcome_administrator/teacher/edit/<int:teacher_id>/', edit_teacher, name='edit_teacher'),
    path('admin/', admin.site.urls),
]
