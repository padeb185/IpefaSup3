from IpefaSup3.models import Student, Teacher, Educator


def get_logged_user_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']  # Correction ici : utiliser des crochets []

        # Vérification dans les modèles (Student, Teacher, Educator)
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



# IpefaSup3/utils.py

import re
from django.core.exceptions import ValidationError

def validate_student_email(email):
    pattern = r"^[a-z]+\.[a-z]+@student\.efpl\.be$"
    if not re.match(pattern, email):
        raise ValidationError("L'adresse email doit être du type nom.prenom@student.efpl.be")
