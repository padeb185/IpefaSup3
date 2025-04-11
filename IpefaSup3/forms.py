
from django import forms


from .models import  Educator,  Teacher, Student, Administrator, AcademicUE, UE

from django.contrib.auth.hashers import make_password, check_password
from .utils import validate_efpl_email, validate_efpl_student_email, get_logged_user_from_request, \
    validate_efpl_email_or_student_email


def clean_email(self):
    email = self.cleaned_data['email']
    if not email.endswith('@student.efpl.be'):
        raise forms.ValidationError("Email invalide.")
    return email


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



class AddStudentForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Student
        exclude = {}
    def clean(self):
        cleaned_data = super(AddStudentForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne corespondent pas")
        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        if self.cleaned_data["password"]:
            student.password = make_password(self.cleaned_data["password"])
        if commit:
            student.save()
        return student

class AddTeacherForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        exclude = {}
    def clean(self):
        cleaned_data = super(AddTeacherForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne corespondent pas")
        return cleaned_data

    def save(self, commit=True):
        teacher = super().save(commit=False)
        if self.cleaned_data["password"]:
            teacher.password = make_password(self.cleaned_data["password"])
        if commit:
            teacher.save()
        return teacher


class AddAdministratorForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Administrator
        exclude = {}
    def clean(self):
        cleaned_data = super(AddAdministratorForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne corespondent pas")
        return cleaned_data

    def save(self, commit=True):
        administrator = super().save(commit=False)
        if self.cleaned_data["password"]:
            administrator.password = make_password(self.cleaned_data["password"])
        if commit:
            administrator.save()
        return administrator



class AddEducatorForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Educator
        exclude = {}
    def clean(self):
        cleaned_data = super(AddEducatorForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne corespondent pas")
        return cleaned_data

    def save(self, commit=True):
        educator = super().save(commit=False)
        if self.cleaned_data["password"]:
            educator.password = make_password(self.cleaned_data["password"])
        if commit:
            educator.save()
        return educator



class AddAcademicUEForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # on récupère request si fourni
        super().__init__(*args, **kwargs)

        if self.request:
            from .utils import get_logged_user_from_request
            logged_user = get_logged_user_from_request(self.request)

    class Meta:
        model = AcademicUE
        fields = '__all__'
        exclude = {}


class AddUEForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # on récupère request si fourni
        super().__init__(*args, **kwargs)

        if self.request:
            from .utils import get_logged_user_from_request
            logged_user = get_logged_user_from_request(self.request)

    class Meta:
        model = UE
        fields = '__all__'
        exclude = {}


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Mot de passe')
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label='Confirmer le mot de passe')

    def __init__(self, *args, **kwargs):
        # Récupérer 'request' si fourni
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            from .utils import get_logged_user_from_request
            logged_user = get_logged_user_from_request(self.request)
            # Tu peux utiliser logged_user ici si nécessaire pour personnaliser le formulaire

    class Meta:
        model = Student
        fields = '__all__'  # Corriger la syntaxe

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Vérifie si le mot de passe et la confirmation sont identiques
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')

        # Si un mot de passe est fourni, le sécuriser
        if password:
            cleaned_data['password'] = make_password(password)  # Utiliser make_password pour sécuriser le mot de passe

        # Sauvegarder l'objet Student avec les données nettoyées
        return super().save(commit)  # Appelle la méthode save() de la classe parente