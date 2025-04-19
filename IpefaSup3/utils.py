from django.core.exceptions import ValidationError
import re
from IpefaSup3.models import Student, Teacher, Educator


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
    if 'logged_user_id' in request.session:
        logged_user_id = request.session('logged_user_id')

        if len(Student.objects.filter(id=logged_user_id)) == 1:
            return Student.objects.get(id=logged_user_id)

        elif len(Teacher.objects.filter(id=logged_user_id)) == 1:
            return Teacher.objects.get(id=logged_user_id)

        elif len(Educator.objects.filter(id=logged_user_id)) == 1:
            return Educator.objects.get(id=logged_user_id)
        else:
            return None
    else:
        return None

