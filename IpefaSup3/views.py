from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string

from .forms import LoginForm, AddStudentForm, AddTeacherForm, AddAdministratorForm, AddAcademicUEForm, AddUEForm, \
    StudentProfileForm, AddEducatorForm, TeacherProfileForm
from .models import Educator, Student, Teacher, Administrator  # Assure-toi d'importer ton modèle Educator
from django.shortcuts import render
from .utils import get_logged_user_from_request


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
            return render(request,'edcucator/welcomeEducator.html' )
        elif logged_user.person_type == 'administrateur':
            return render(request, 'admin/welcomeAdmin.html',
                          {'logged_user': logged_user})
        else:
            return redirect('/login')
    else:
        return redirect('/login')



def login(request):
    if len(request.POST) > 0:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            if user_email:
                logged_user = Student.objects.get(email=user_email)
                request.session['logged_user_id'] = logged_user.id
                return redirect('/welcome')
            else:
                # Cas où on vérifie le matricule
                user_matricule = form.cleaned_data['matricule']
                if user_matricule:
                    try:
                        logged_user = Teacher.objects.get(matricule=user_matricule)
                        request.session['logged_user_id'] = logged_user.id
                        return redirect('/welcome')
                    except Teacher.DoesNotExist:
                        # Gérer l'exception si le matricule n'est pas trouvé dans Teacher
                        form.add_error('matricule', 'Matricule non trouvé.')
                else:
                    # Cas pour Educator
                    try:
                        logged_user = Educator.objects.get(matricule=user_matricule)
                        request.session['logged_user_id'] = logged_user.id
                        return redirect('/welcome')
                    except Educator.DoesNotExist:
                        # Gérer l'exception si le matricule n'est pas trouvé dans Educator
                        form.add_error('matricule', 'Matricule non trouvé.')

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

    return render(request, 'welcome_administrator/../templates/admin/add_academic_ue.html', {
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

        return render(request, 'welcome_administrator/../templates/admin/add_ue.html',
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

        return render(request, 'admin/student_list.html',
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

        return render(request, 'admin/edit_student.html', {'form': form, 'student': student, 'logged_user': logged_user, 'current_date_time': datetime.now})

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

        return render(request, 'welcome_administrator/../templates/admin/teacher_list.html', {'teachers': teachers, 'logged_user': logged_user, 'current_date_time': datetime.now})

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

        return render(request, 'welcome_administrator/../templates/admin/edit_teacher.html', {'form': form, 'teacher': teacher, 'logged_user': logged_user, 'current_date_time': datetime.now})
