from datetime import datetime
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .forms import LoginForm, AddStudentForm, AddTeacherForm, AddAdministratorForm, AddAcademicUEForm, AddUEForm, \
    StudentForm, AddEducatorForm
from .models import Educator, Student, Teacher, Administrator  # Assure-toi d'importer ton modèle Educator





# views.py
from django.shortcuts import render

from .utils import get_logged_user_from_request


def welcome(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        return render(request, 'welcome.html', {'logged_user': logged_user, 'current_date_time': datetime.now()})
    else:
        return render(request, 'login.html')  # pas de slash initial ici



def welcome_student(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        return render(request, 'welcome_student.html', {'logged_user': logged_user, 'current_date_time': datetime.now()} )
    else:
        return render(request, 'login.html')  # pas de slash initial ici



def welcome_teacher(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        return render(request, 'welcome_teacher.html', {'logged_user': logged_user, 'current_date_time': datetime.now()} )
    else:
        return render(request, 'login.html')  # pas de slash initial ici



def welcome_administrator(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
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
                    return render(request, 'welcome_teacher.html', {
                        'logged_user': logged_user,
                        'current_date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })  # # Page pour le professeur
                elif Educator.objects.filter(employee_email=user_email).exists():
                    logged_user = Educator.objects.get(employee_email=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return render(request,  'welcome.html', {
                        'logged_user': logged_user,
                        'current_date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })# Page pour l'éducateur
                elif Administrator.objects.filter(employee_email=user_email).exists():
                    logged_user = Administrator.objects.get(employee_email=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return render(request, 'welcome_administrator.html', {
                        'logged_user': logged_user,
                        'current_date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })  #
                    # Page pour l'administrateur
                # Cherche dans le modèle Student
                elif Student.objects.filter(studentMail=user_email).exists():
                    logged_user = Student.objects.get(studentMail=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return render(request, 'welcome_student.html', {
                        'logged_user': logged_user,
                        'current_date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })  # # Page pour l'étudiant
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
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if request.method == "POST":
            form = AddStudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/welcome')  # Redirection après ajout réussi
        else:
            form = AddStudentForm()  # Initialisation propre du formulaire

        return render(request, 'welcome/add_student.html', {'form': form,  'logged_user': logged_user, 'current_date_time': datetime.now})

def add_educator_views(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if request.method == "POST":
            form = AddEducatorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/welcome')  # Redirection après ajout réussi
        else:
            form = AddEducatorForm()  # Initialisation propre du formulaire

        return render(request, 'welcome_administrator/add_educator.html', {'form': form, 'logged_user': logged_user, 'current_date_time': datetime.now})


def add_teacher_views(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if request.method == "POST":
            form = AddTeacherForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/welcome_administrator')  # Redirection après ajout réussi
        else:
            form = AddTeacherForm()  # Initialisation propre du formulaire

        return render(request, 'welcome_administrator/add_teacher.html', {'form': form, 'logged_user': logged_user, 'current_date_time': datetime.now})


def add_administrator_views(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if request.method == "POST":
            form = AddAdministratorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/welcome_administrator')  # Redirection après ajout réussi
        else:
            form = AddAdministratorForm()  # Initialisation propre du formulaire

        return render(request, 'welcome_administrator/add_administrator.html', {'form': form, 'logged_user': logged_user, 'current_date_time': datetime.now})

def add_academic_ue_views(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if request.method == 'POST':
            form = AddAcademicUEForm(request.POST)
            if form.is_valid():
                form.save()  # Sauvegarde les données si le formulaire est valide
                # Rediriger ou renvoyer une réponse après soumission
        else:
            form = AddAcademicUEForm()  # Crée une nouvelle instance du formulaire

    return render(request, 'welcome_administrator/add_academic_ue.html', {'form': form, 'logged_user': logged_user, 'current_date_time': datetime.now})

def add_ue_views(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if request.method == 'POST':
            form = AddUEForm(request.POST)
            if form.is_valid():
                form.save()  # Sauvegarde les données si le formulaire est valide
                # Rediriger ou renvoyer une réponse après soumission
        else:
            form = AddUEForm()  # Crée une nouvelle instance du formulaire

        return render(request, 'welcome_administrator/add_ue.html', {'form': form, 'logged_user': logged_user, 'current_date_time': datetime.now})




def student_list(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        sort_by = request.GET.get('sort_by', None)

        if sort_by == 'first_name':
            students = Student.objects.all().order_by('first_name')
        elif sort_by == 'last_name':
            students = Student.objects.all().order_by('last_name')
        else:
            students = Student.objects.all()

        return render(request, 'student_list.html', {'students': students, 'logged_user': logged_user, 'current_date_time': datetime.now})

def edit_student(request, student_id):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        student = get_object_or_404(Student, id=student_id)

        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()  # Sauvegarder les modifications de l'étudiant
                return redirect('student_list')  # Rediriger vers la liste après la mise à jour
        else:
            form = StudentForm(instance=student)

        return render(request, 'edit_student.html', {'form': form, 'student': student,'logged_user': logged_user, 'current_date_time': datetime.now})

def teacher_list(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        sort_by = request.GET.get('sort_by', None)

        if sort_by == 'first_name':
            teachers = Teacher.objects.all().order_by('first_name')
        elif sort_by == 'last_name':
            teachers = Teacher.objects.all().order_by('last_name')
        else:
            teachers = Teacher.objects.all()

        return render(request, 'teacher_list.html', {'teachers': teachers, 'logged_user': logged_user, 'current_date_time': datetime.now})