from itertools import chain
from django import forms
from .models import Person, Educator, Employee, Teacher, Student, Administrator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .utils import validate_efpl_email, validate_efpl_student_email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Courriel", required=True, validators=[validate_efpl_email])
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

