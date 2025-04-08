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

        # Vérifie que les deux champs sont valides
        if email and password:
            educator_queryset = Educator.objects.filter(Q(password=password) & Q(employee_email=email))
            teacher_queryset = Teacher.objects.filter(Q(password=password) & Q(employee_email=email))
            administrator_queryset = Administrator.objects.filter(Q(password=password) & Q(employee_email=email))
            student_queryset = Student.objects.filter(Q(password=password) & Q(studentMail=email))

            # Combinez les résultats avec `chain`
            result = list(chain(educator_queryset, teacher_queryset, administrator_queryset, student_queryset))
            if len(result) != 1:
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


