from django.shortcuts import render, redirect
from .forms import LoginForm, AddStudentForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Educator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Educator  # Assurez-vous que le modèle est bien importé

def get_logged_user_from_request(request):
    """ Récupère l'éducateur connecté si disponible """
    logged_user_id = request.session.get('logged_user_id')  # Utilisation de .get() pour éviter KeyError

    if logged_user_id:
        return Educator.objects.filter(user_id=logged_user_id).first()  # Retourne None si non trouvé

    return None


@login_required
def welcome(request):

    """ Vue de bienvenue pour l'utilisateur connecté """
    educator = get_logged_user_from_request(request)

    context = {
        'user_id': request.user.id,
        'first_name': request.user.first_name if request.user.first_name else 'Cher éducateur',
        'last_name': request.user.last_name if request.user.last_name else '',
        'is_educator': educator is not None  # Vérifie si l'utilisateur est un éducateur
    }

    return render(request, 'welcome.html', context)




def login(request):
    if len(request.POST)>0:
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('/welcome')
        else:
            return render(request, "login.html", {'form':form})
    else:
        form = LoginForm(request.POST)
        return render(request, "login.html", {'form':form})

@login_required
def add_student_views(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/welcome')  # Redirection après ajout réussi
    else:
        form = AddStudentForm()  # Initialisation propre du formulaire

    return render(request, 'welcome/add_student.html', {'form': form})