from datetime import datetime

from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from .forms import LoginForm, AddStudentForm, AddTeacherForm, AddAdministratorForm, AddAcademicUEForm, AddUEForm, \
    StudentProfileForm, AddEducatorForm, TeacherProfileForm
from .models import Educator, Student, Teacher, Administrator, \
    validate_student_email
from django.shortcuts import render
from .utils import get_logged_user_from_request


def welcome(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        if logged_user.person_type == 'etudiant':
            return render(request, 'student/welcomeStudent.html', {'logged_user': logged_user})
        elif logged_user.person_type == 'professeur':
            return render(request, 'teacher/welcomeTeacher.html', {'logged_user': logged_user})
        elif logged_user.person_type == 'Educator':
            return render(request, 'educator/welcomeEducator.html')
        elif logged_user.person_type == 'administrateur':
            return render(request, 'administrator/welcomeAdmin.html', {'logged_user': logged_user})
        else:
            return redirect('/login')  # Cas où le type de personne n'est pas trouvé
    else:
        return redirect('/login')  # Si aucun utilisateur connecté


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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_matricule = form.cleaned_data.get('matricule')
            password = form.cleaned_data.get('password')  # Assure-toi que ce champ est dans ton formulaire

            if user_email:
                if validate_student_email(user_email):
                    try:
                        logged_user = Student.objects.get(studentMail=user_email)
                        if check_password(password, logged_user.password):
                            request.session['logged_user_id'] = logged_user.id
                            return redirect('/welcome')
                        else:
                            form.add_error('password', 'Mot de passe incorrect.')
                    except Student.DoesNotExist:
                        form.add_error('email', 'Aucun étudiant trouvé avec cet email.')
                else:
                    form.add_error('email', 'L\'email n\'est pas valide pour un étudiant.')

            elif user_matricule:
                try:
                    logged_user = get_user_by_matricule(user_matricule)
                    if check_password(password, logged_user.password):
                        request.session['logged_user_id'] = logged_user.id
                        return redirect('/welcome')
                    else:
                        form.add_error('password', 'Mot de passe incorrect.')
                except ValueError as e:
                    form.add_error('matricule', str(e))
            else:
                form.add_error(None, 'Veuillez entrer un email ou un matricule.')
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def register(request):
    if len(request.POST) > 0 and 'profileType' in request.POST:
        studentForm = AddStudentForm(prefix="st")
        teacherForm = AddTeacherForm(prefix="te")
        educatorForm = AddEducatorForm(prefix="ed")
        administratorForm = AddAdministratorForm(prefix="ad")
        if request.POST['profileType'] == 'Student':
            if studentForm.is_valid():
                studentForm.save()
                return redirect('/login')
        elif request.POST['profileType'] == 'Teacher':
            if teacherForm.is_valid():
                teacherForm.save()
                return redirect('/login')
        elif request.POST['profileType'] == 'Educator':
            if educatorForm.is_valid():
                educatorForm.save()
                return redirect('/login')
        elif request.POST['profileType'] == 'Administrator':
            if administratorForm.is_valid():
                administratorForm.save()
                return redirect('/login')
        return render(request, 'user_profile.html',
                      {'studentForm': studentForm, 'teacherForm': teacherForm,
                       'educatorForm': educatorForm, 'administratorForm': administratorForm})

    else:
        studentForm = AddStudentForm(prefix="st")
        teacherForm = AddTeacherForm(prefix="te")
        educatorForm = AddEducatorForm(prefix="ed")
        administratorForm = AddAdministratorForm(prefix="ad")
        return render(request, 'user_profile.html',
                      {'studentForm': studentForm, 'teacherForm': teacherForm,
                       'educatorForm': educatorForm,'administratorForm': administratorForm})




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
