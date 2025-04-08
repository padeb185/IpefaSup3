from datetime import datetime
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import LoginForm, AddStudentForm, AddTeacherForm
from .models import Educator, Student, Teacher, Administrator  # Assure-toi d'importer ton modèle Educator





# views.py
from django.shortcuts import render


def get_logged_user_from_request(request):
    user_id = request.session.get('logged_user_id')
    if not user_id:
        return None
    # Recherche l'utilisateur avec l'ID
    user = None
    if Student.objects.filter(id=user_id).exists():
        user = Student.objects.get(id=user_id)
    elif Teacher.objects.filter(id=user_id).exists():
        user = Teacher.objects.get(id=user_id)
    elif Educator.objects.filter(id=user_id).exists():
        user = Educator.objects.get(id=user_id)

    return user


def welcome(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session.get('logged_user_id')
        logged_user = Educator.objects.get(id=logged_user_id)# utilise .get() pour éviter KeyError
        return render(request, 'login/../templates/welcome.html', {'logged_user': logged_user, 'current_date_time': datetime.now()})
    else:
        return render(request, 'login.html')  # pas de slash initial ici



def welcome_student(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session.get('logged_user_id')
        logged_user = Student.objects.get(id=logged_user_id)# utilise .get() pour éviter KeyError
        return render(request, 'welcome_student.html', {'logged_user': logged_user, 'current_date_time': datetime.now()} )
    else:
        return render(request, 'login.html')  # pas de slash initial ici



def welcome_teacher(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session.get('logged_user_id')
        logged_user = Teacher.objects.get(id=logged_user_id)# utilise .get() pour éviter KeyError
        return render(request, 'welcome_teacher.html', {'logged_user': logged_user, 'current_date_time': datetime.now()} )
    else:
        return render(request, 'login.html')  # pas de slash initial ici



def welcome_administrator(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session.get('logged_user_id')
        logged_user = Administrator.objects.get(id=logged_user_id)# utilise .get() pour éviter KeyError
        return render(request, 'welcome_administrator.html', {'logged_user': logged_user, 'current_date_time': datetime.now()} )
    else:
        return render(request, 'login.html')  # pas de slash initial ici





def login(request):
    if len(request.POST) > 0:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']

            # Vérification de l'existence de l'utilisateur et redirection en fonction du rôle
            try:
                # Cherche dans les modèles Teacher, Educator et Administrator
                if Teacher.objects.filter(employee_email=user_email).exists():
                    logged_user = Teacher.objects.get(employee_email=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return render(request, 'welcome_teacher.html')  # Page pour le professeur
                elif Educator.objects.filter(employee_email=user_email).exists():
                    logged_user = Educator.objects.get(employee_email=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return render(request,  'welcome.html')  # Page pour l'éducateur
                elif Administrator.objects.filter(employee_email=user_email).exists():
                    logged_user = Administrator.objects.get(employee_email=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return render(request, 'welcome_administrator.html')  # Page pour l'administrateur
                # Cherche dans le modèle Student
                elif Student.objects.filter(studentMail=user_email).exists():
                    logged_user = Student.objects.get(studentMail=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return render(request, 'welcome_student.html')  # Page pour l'étudiant
                else:
                    return HttpResponse("Utilisateur non trouvé", status=404)  # Utilisateur non trouvé
            except Exception as e:
                return HttpResponse(f"Erreur : {e}", status=500)

        else:
            return render(request, "login.html", {'form': form})
    else:
        form = LoginForm()
        return render(request, "login.html", {'form': form})




def add_student_views(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/welcome')  # Redirection après ajout réussi
    else:
        form = AddStudentForm()  # Initialisation propre du formulaire

    return render(request, 'welcome/add_student.html', {'form': form})

def add_teacher_views(request):
    if request.method == "POST":
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/welcome')  # Redirection après ajout réussi
    else:
        form = AddTeacherForm()  # Initialisation propre du formulaire

    return render(request, 'welcome_administrator/add_teacher.html', {'form': form})


