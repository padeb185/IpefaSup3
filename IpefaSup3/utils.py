from django.core.exceptions import ValidationError
import re

from IpefaSup3.models import Student, Teacher, Educator


def validate_efpl_email(value):
    if not re.match(r'^[a-zA-Z]+\.[a-zA-Z]+@efpl\.be$', value):
        raise ValidationError("Email doit être au format prénom.nom@efpl.be")



def validate_efpl_student_email(value):
    if not re.match(r'^[a-zA-Z]+\.[a-zA-Z]+@sqtudent\.efpl\.be$', value):
        raise ValidationError("Email doit être au format prénom.nom@student.efpl.be")


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

    return user
