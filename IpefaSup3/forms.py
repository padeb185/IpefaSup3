from django import forms
from .models import  Educator,  Teacher, Student, Administrator, AcademicUE, UE
from django.contrib.auth.hashers import make_password, check_password
from .utils import validate_efpl_email_or_student_email, get_logged_user_from_request


class LoginForm(forms.Form):
    email = forms.EmailField(label="Courriel", required=True, validators=[validate_efpl_email_or_student_email])
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = None

            # Recherche dans Educator
            for educator in Educator.objects.filter(employee_email=email):
                if check_password(password, educator.password):
                    user = educator
                    break

            # Recherche dans Teacher
            if not user:
                for teacher in Teacher.objects.filter(employee_email=email):
                    if check_password(password, teacher.password):
                        user = teacher
                        break

            # Recherche dans Administrator
            if not user:
                for admin in Administrator.objects.filter(employee_email=email):
                    if check_password(password, admin.password):
                        user = admin
                        break

            # Recherche dans Student
            if not user:
                for student in Student.objects.filter(studentMail=email):
                    if check_password(password, student.password):
                        user = student
                        break

            if not user:
                raise forms.ValidationError("Adresse de courriel ou mot de passe erroné.")

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

    def check_if_admin(self):
        logged_user = get_logged_user_from_request(self.request)
        if not logged_user or not isinstance(logged_user, Administrator):
            raise PermissionError("Accès réservé aux administrateurs")

    @property
    def model_name(self):
        return self._meta.model.__name__


class AddStudentForm(BaseListForm):

    class Meta:
        model = Student
        exclude = {}

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
                raise PermissionError("Accès réservé uniquement aux administrateurs et Educateurs")



class AddTeacherForm(BaseListForm):

    class Meta:
        model = Teacher
        exclude = {}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.check_if_admin()



class AddAdministratorForm(BaseListForm):
    class Meta:
        model = Administrator
        exclude = {}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.check_if_admin()






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
