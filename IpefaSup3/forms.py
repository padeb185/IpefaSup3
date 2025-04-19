from django import forms
from .models import  Educator,  Teacher, Student, Administrator, AcademicUE, UE
from django.contrib.auth.hashers import make_password, check_password
from .utils import get_logged_user_from_request, validate_student_email

from django import forms
from django.contrib.auth.hashers import check_password
from .models import Student, Teacher, Educator


class LoginForm(forms.Form):
    matricule = forms.CharField(label='Matricule', required=False)
    email = forms.EmailField(label="Courriel", required=False, validators=[validate_student_email])
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        matricule = cleaned_data.get("matricule")

        if email and password:
            try:
                student = Student.objects.get(studentMail=email)
                if not check_password(password, student.password):
                    raise forms.ValidationError("Adresse mail ou mot de passe incorrect")
            except Student.DoesNotExist:
                raise forms.ValidationError("Adresse mail ou mot de passe incorrect")

        elif matricule and password:
            user = None
            try:
                user = Teacher.objects.get(matricule=matricule.strip())
            except Teacher.DoesNotExist:
                try:
                    user = Educator.objects.get(matricule=matricule.strip())
                except Educator.DoesNotExist:
                    raise forms.ValidationError("Matricule ou mot de passe incorrect")

            if not check_password(password, user.password):
                raise forms.ValidationError("Matricule ou mot de passe incorrect")

        else:
            raise forms.ValidationError("Veuillez entrer un email ou un matricule avec le mot de passe.")

        return cleaned_data




class BaseListForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Mot de passe')
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label='Confirmer le mot de passe')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne corespondent pas")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data["password"]:
            instance.password = make_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance




class AddStudentForm(BaseListForm):

    class Meta:
        model = Student
        exclude = {}




class AddTeacherForm(BaseListForm):

    class Meta:
        model = Teacher
        exclude = {}



class AddAdministratorForm(BaseListForm):
    class Meta:
        model = Administrator
        exclude = {}




class AddEducatorForm(BaseListForm):

    class Meta:
        model = Educator
        exclude = {}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.check_if_admin()


class AddAcademicUEForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # On récupère `request` si fourni
        super().__init__(*args, **kwargs)

        if self.request:
            logged_user = get_logged_user_from_request(self.request)

            # Vérification que l'utilisateur est bien un administrateur
            if not logged_user or not isinstance(logged_user, Administrator):
                # Si l'utilisateur n'est pas un administrateur, on peut lever une exception ou rediriger
                raise PermissionError("Accès réservé uniquement aux administrateurs")

    class Meta:
        model = AcademicUE
        fields = '__all__'  # Pas besoin de `exclude = {}` si on utilise `fields = '__all__'`


class AddUEForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # On récupère `request` si fourni
        super().__init__(*args, **kwargs)

        if self.request:
            from .utils import get_logged_user_from_request
            logged_user = get_logged_user_from_request(self.request)

            # Vérification que l'utilisateur est bien un administrateur
            if not logged_user or not isinstance(logged_user, Administrator):
                # Si l'utilisateur n'est pas un administrateur, on peut lever une exception ou rediriger
                raise PermissionError("Accès réservé uniquement aux administrateurs")
    class Meta:
        model = UE
        fields = '__all__'





class StudentProfileForm(BaseListForm):#liste des étudiants

    def __init__(self, *args, **kwargs):
        # Récupérer 'request' si fourni
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            from .utils import get_logged_user_from_request
            logged_user = get_logged_user_from_request(self.request)

            # Vérification que l'utilisateur est soit un Administrator soit un Teacher
            if not logged_user or not isinstance(logged_user, (Administrator, Educator)):
                # Si l'utilisateur n'est pas un Administrator ou un Teacher, on l'empêche d'accéder
                raise PermissionError("Accès réservé uniquement aux administrateurs et éducateur")

    class Meta:
        model = Student
        fields = '__all__'  # Corriger la syntaxe



class TeacherProfileForm(BaseListForm):

    def __init__(self, *args, **kwargs):
        # Récupérer 'request' si fourni
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            from .utils import get_logged_user_from_request
            logged_user = get_logged_user_from_request(self.request)

            # Vérification que l'utilisateur est soit un Administrator soit un Teacher
            if not logged_user or not isinstance(logged_user, Administrator):
                # Si l'utilisateur n'est pas un Administrator ou un Teacher, on l'empêche d'accéder
                raise PermissionError("Accès réservé uniquement aux administrateurs ")

    class Meta:
        model = Teacher
        fields = '__all__'  # Corriger la syntaxe
