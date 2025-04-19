from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import LoginForm, AddStudentForm, AddTeacherForm, AddAdministratorForm, AddAcademicUEForm, AddUEForm, \
    StudentProfileForm, AddEducatorForm, TeacherProfileForm
from .models import Educator, Student, Teacher, Administrator  # Assure-toi d'importer ton modèle Educator
from django.shortcuts import render
from .utils import get_logged_user_from_request, validate_student_email


def welcome(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if logged_user.person_type == 'etudiant':
            return render(request, 'student/welcomeStudent.html',
                          {'logged_user': logged_user})
        elif logged_user.person_type == 'professeur':
            return render(request, 'teacher/welcomeTeacher.html',
                          {'logged_user': logged_user})
        elif logged_user.person_type == 'Educator':
            return render(request,'educator/welcomeEducator.html' )
        elif logged_user.person_type == 'administrateur':
            return render(request, 'administrator/welcomeAdmin.html',
                          {'logged_user': logged_user})
        else:
            return redirect('/login')
    else:
        return redirect('/login')
def get_user_by_matricule(matricule):
    try:
        # Essayer de récupérer l'utilisateur par matricule, vérifier dans Teacher, puis Educator
        return Teacher.objects.get(matricule=matricule)
    except Teacher.DoesNotExist:
        try:
            return Educator.objects.get(matricule=matricule)
        except Educator.DoesNotExist:
            raise ValueError('Matricule non trouvé.')  # Lever une exception si aucune correspondance


def login(request):
    if len(request.POST) > 0:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_matricule = form.cleaned_data.get('matricule')

            if user_email:
                # Vérification si l'email est valide pour un étudiant
                if validate_student_email(user_email):
                    # Si l'email est valide, essayer de trouver un Student avec cet email
                    logged_user = get_object_or_404(Student, studentMail=user_email)
                    request.session['logged_user_id'] = logged_user.id
                    return redirect('/welcome')
                else:
                    form.add_error('email', 'L\'email n\'est pas valide pour un étudiant.')
            elif user_matricule:
                # Si le matricule est fourni, chercher l'utilisateur
                try:
                    logged_user = get_user_by_matricule(user_matricule)
                    request.session['logged_user_id'] = logged_user.id
                    return redirect('/welcome')
                except ValueError as e:
                    # Ajouter l'erreur de matricule non trouvé
                    form.add_error('matricule', str(e))
            else:
                form.add_error(None, 'Veuillez entrer un email ou un matricule.')  # Erreur si rien n'est entré

        # Si le formulaire n'est pas valide ou s'il n'y a pas de correspondance
        return render(request, 'login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def add_academic_ue_views(request):
    logged_user = get_logged_user_from_request(request)
    if not logged_user:
        return redirect('login')  # Ou une autre redirection en cas d'absence d'utilisateur connecté

    if request.method == 'POST':
        form = AddAcademicUEForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Remplace par la page vers laquelle tu veux rediriger après ajout
    else:
        form = AddAcademicUEForm()

    return render(request, 'administrator/add_academic_ue.html', {
        'form': form,
        'logged_user': logged_user,
        'current_date_time': datetime.now(),
    })


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

        return render(request, 'administrator/add_ue.html',
                      {'form': form, 'logged_user': logged_user, 'current_date_time': datetime.now})




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

        return render(request, 'administrator/student_list.html',
                      {'students': students, 'logged_user': logged_user, 'current_date_time': datetime.now})

def edit_student(request, student_id):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        student = get_object_or_404(Student, id=student_id)

        if request.method == 'POST':
            form = StudentProfileForm(request.POST, instance=student)
            if form.is_valid():
                form.save()  # Sauvegarder les modifications de l'étudiant
                return redirect('student_list')  # Rediriger vers la liste après la mise à jour
        else:
            form = StudentProfileForm(instance=student)

        return render(request, 'administrator/edit_student.html', {'form': form, 'student': student, 'logged_user': logged_user, 'current_date_time': datetime.now})

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

        return render(request, 'administrator/teacher_list.html', {'teachers': teachers, 'logged_user': logged_user, 'current_date_time': datetime.now})

def edit_teacher(request, teacher_id):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        teacher = get_object_or_404(Teacher, id=teacher_id)

        if request.method == 'POST':
            form = TeacherProfileForm(request.POST, instance=teacher)
            if form.is_valid():
                form.save()  # Sauvegarder les modifications de l'étudiant
                return redirect('teacher_list')  # Rediriger vers la liste après la mise à jour
        else:
            form = TeacherProfileForm(instance=teacher)

        return render(request, 'administrator/edit_teacher.html', {'form': form, 'teacher': teacher, 'logged_user': logged_user, 'current_date_time': datetime.now})
