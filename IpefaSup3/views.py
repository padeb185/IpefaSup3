from django.contrib.auth.hashers import check_password
from django.shortcuts import  redirect
from .forms import LoginForm, AddStudentForm, LoginFormStudent
from .models import Educator, Student, Teacher  # Assure-toi d'importer ton modèle Educator


# views.py
from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil.html')

def etudiant_view(request):
    return render(request, 'etudiant.html')

def educateur_view(request):
    return render(request, 'educateur.html')

def professeur_view(request):
    return render(request, 'professeur.html')



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
        return render(request, 'welcome.html', {'logged_user': logged_user})
    else:
        return render(request, 'login.html')  # pas de slash initial ici





def login(request):
    if len(request.POST)>0:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            logged_user = Educator.objects.get(employee_email=user_email)
            request.session['logged_user_id'] = logged_user.id
            return redirect('/welcome')
        else:
            return render(request, "login.html", {'form':form})
    else:
        form = LoginForm(request.POST)
        return render(request, "login.html", {'form':form})


def login_etudiant(request):
    if request.method == "POST":
        form = LoginFormStudent(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            logged_user = Student.objects.get(student_email=user_email)
            request.session['logged_user_id'] = logged_user.id
            return redirect('/welcome_etudiant')#Redirige vers la page de bienvenue
        else:
            return render(request, "login.etudiant.html", {'form': form})
    else:
            form = LoginForm(request.POST)
            return render(request, "login.etudiant.html", {'form': form})


def login_professeur(request):
    if len(request.POST)>0:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            logged_user = Teacher.objects.filter(employee_email=user_email).first()
            request.session['logged_user_id'] = logged_user.id
            return redirect('/welcome/professeur')
        else:
            return render(request, "login.professeur.html", {'form':form})
    else:
        form = LoginForm(request.POST)
        return render(request, "login.professeur.html", {'form':form})



def add_student_views(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/welcome')  # Redirection après ajout réussi
    else:
        form = AddStudentForm()  # Initialisation propre du formulaire

    return render(request, 'welcome/add_student.html', {'form': form})



def welcome_etudiant(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session.get('logged_user_id')
        logged_user = Student.objects.get(id=logged_user_id)# utilise .get() pour éviter KeyError
        return render(request, 'welcome_etudiant.html', {'logged_user': logged_user})
    else:
        return render(request, 'login.etudiant.html')  # pas de slash initial ici
