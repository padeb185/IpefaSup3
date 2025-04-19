from django.core.exceptions import ValidationError
import re
from IpefaSup3.models import Student, Teacher, Educator

import re


def validate_student_email(email):
    # Expression régulière pour valider le format nom.prenom@student.efpl.be
    pattern = r'^[a-zA-Z]+(\.[a-zA-Z]+)*@student\.efpl\.be$'
    return bool(re.match(pattern, email))


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

