from django.core.exceptions import ValidationError
import re

from django.shortcuts import redirect

from IpefaSup3.models import Student, Teacher, Educator, Administrator


def validate_efpl_email(value):
    pattern = r'^[a-zA-Z]+\.[a-zA-Z]+@efpl\.be$'
    if not re.match(pattern, value):
        raise ValidationError("L'adresse doit être du type nom.prenom@efpl.be.")

def validate_efpl_student_email(value):
    pattern = r'^[a-zA-Z]+\.[a-zA-Z]+@student\.efpl\.be$'
    if not re.match(pattern, value):
        raise ValidationError("L'adresse doit être du type nom.prenom@student.efpl.be.")


def validate_efpl_email_or_student_email(value):
    try:
        validate_efpl_email(value)
    except ValidationError:
        try:
            validate_efpl_student_email(value)
        except ValidationError:
            raise ValidationError("L'adresse doit être une adresse EFPL ou EFPL étudiant.")


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
    elif Administrator.objects.filter(id=user_id).exists():
        user = Administrator.objects.get(id=user_id)

    return user

