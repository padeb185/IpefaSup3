from django.core.exceptions import ValidationError
import re

def validate_efpl_email(value):
    if not re.match(r'^[a-zA-Z]+\.[a-zA-Z]+@efpl\.be$', value):
        raise ValidationError("Email doit être au format prénom.nom@efpl.be")



def validate_efpl_student_email(value):
    if not re.match(r'^[a-zA-Z]+\.[a-zA-Z]+@sqtudent\.efpl\.be$', value):
        raise ValidationError("Email doit être au format prénom.nom@student.efpl.be")

