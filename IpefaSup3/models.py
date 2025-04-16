from django.core.exceptions import ValidationError
from django.db import models
import re



def custom_email_validator(value):
    pattern = r'^[a-zA-Z]+\.[a-zA-Z]+@(student\.)?efpl\.be$'
    if not re.match(pattern, value):
        raise ValidationError(
            "L'adresse email doit être au format nom.prenom@efpl.be ou nom.prenom@student.efpl.be"
        )


class Person(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    private_email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


    class Meta:
        abstract = True  # Empêche la création de la table Employee



class Employee(Person):
    employee_email = models.EmailField(unique=True)
    matricule = models.CharField(max_length=255)


    class Meta:
        abstract = True  # Empêche la création de la table Employee




class Teacher(Employee):
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.employee_email}"





class Educator(Employee):
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.employee_email}"



class Administrator(Employee):  # Hérite de Employee
    # Vous pouvez ajouter des attributs ou méthodes spécifiques aux administrateurs
    role = models.CharField(max_length=100, default="Administrator")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"




class Student(Person):  # Hérite de Person
    studentMail = models.EmailField(validators=[custom_email_validator], unique=True)  # Email étudiant
    sessions = models.ManyToManyField('Session', related_name='students',
                                      blank=True)  # Relation ManyToMany avec Session
    academic_ues = models.ManyToManyField('AcademicUE', related_name='students',
                                          blank=True)  # Relation ManyToMany avec AcademicUE
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.studentMail})"


# Création d'un étudiant
#student = Student.objects.create(
#    first_name="John",
#    last_name="Doe",
#    email="john.doe@example.com",
#    studentMail="johndoe@student.university.com"
#)

# Création d'une section
#section = Section.objects.create(wording="Sciences")

# Création d'AcademicUE
#math_ue = AcademicUE.objects.create(idUE="MATH101", wording="Mathématiques", numberPeriods=30,
            #                        section=section, academicYear="2024-2025", yearCycle=1)

#physics_ue = AcademicUE.objects.create(idUE="PHYS101", wording="Physique", numberPeriods=40,
#                                       section=section, academicYear="2024-2025", yearCycle=1)

# Inscrire l'étudiant à ces UE
#student.academic_ues.add(math_ue, physics_ue)

# Vérifier les UE d'un étudiant
#for ue in student.academic_ues.all():
#    print(ue)

# Vérifier les étudiants inscrits dans une UE
#for stud in math_ue.students.all():
#    print(stud)

#Résultat attendu

#MATH101 - Mathématiques (2024-2025, Cycle 1)
#PHYS101 - Physique (2024-2025, Cycle 1)
#John Doe (johndoe@student.university.com)

#✅ Cette implémentation respecte bien la relation ManyToMany entre Student et AcademicUE !
#Besoin d'un ajustement ou d'une contrainte supplémentaire ? 🚀😊





class Section(models.Model):
    wording = models.CharField(max_length=255)

    def __str__(self):
        return self.wording


#Une Section a un wording (nom ou description).

#Une UE (Unité d'Enseignement) a plusieurs attributs (idUE, wording, numberPeriods).

#Une Section peut être associée à plusieurs UEs (relation 0,N).

#Une UE peut avoir plusieurs prérequis (relation récursive 0,N).



class UE(models.Model):
    idUE = models.CharField(max_length=50, unique=True)
    wording = models.CharField(max_length=255)
    numberPeriods = models.IntegerField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='ues')  # Relation 0,N avec Section
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependents')  # Relation récursive 0,N

    def __str__(self):
        return f"{self.idUE} - {self.wording} - {self.numberPeriods} - {self.section} - {self.prerequisites}"

#Avec cette approche, tu peux récupérer :

 #   Toutes les UEs d'une section : section_instance.ues.all()

 #   Les prérequis d'une UE : ue_instance.prerequisites.all()

 #   Les UEs qui dépendent d'une UE donnée : ue_instance.dependents.all()



class AcademicUE(UE):  # Hérite de UE
    academicYear = models.CharField(max_length=9)  # Ex: "2024-2025"
    yearCycle = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='academic_ues')  # Relation 0,1 vers Teacher
    def type(self):
        return "Academic UE"

    def __str__(self):
        return f"{self.idUE} - {self.wording} ({self.academicYear}, Cycle {self.yearCycle})"


#Si tu as un lien de composition (♦ noire) entre AcademicUE et Session, cela signifie que :

 #   Une AcademicUE contient des Sessions.

 #   Une Session ne peut pas exister sans une AcademicUE.

 #   Si une AcademicUE est supprimée, toutes ses Sessions sont supprimées aussi.



class Session(models.Model):
    jour = models.IntegerField()  # 1 à 31
    mois = models.IntegerField()  # 1 à 12
    academicUE = models.ForeignKey(AcademicUE, on_delete=models.CASCADE, related_name='sessions')  # Composition

    def __str__(self):
        return f"Session le {self.jour}/{self.mois} pour {self.academicUE.wording}"



# Création d'une section
# section = Section.objects.create(wording="Sciences")

# Création d'une AcademicUE
# academic_ue = AcademicUE.objects.create(idUE="MATH101", wording="Mathématiques", numberPeriods=30,
                                       # section=section, academicYear="2024-2025", yearCycle=1)

# Ajout de sessions
#session1 = Session.objects.create(jour=15, mois=6, academicUE=academic_ue)
#session2 = Session.objects.create(jour=20, mois=12, academicUE=academic_ue)

# Afficher les sessions d'une UE
#for session in academic_ue.sessions.all():
#    print(session)





# Une classe Participation qui relie Student et Session avec une relation en pointillé indique généralement une association avec une classe intermédiaire (c'est-à-dire une relation ManyToMany avec attributs).

#Dans Django, cela signifie que nous devons remplacer la relation ManyToMany directe entre Student et Session par un modèle Participation qui stockera le statut de la participation.


class Participation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='participations')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='participations')
    status = models.CharField(max_length=50, choices=[("P", "Présentiel"), ("M", "distanciel"), ("A", "absence"), ("CM", "CM"), ("abandon", "abandon"), ("dispense", "dispense")])

    def __str__(self):
        return f"{self.student} - {self.session} ({self.status})"


# Création d'un étudiant
#student = Student.objects.create(
#    first_name="John",
#    last_name="Doe",
#    email="john.doe@example.com",
#    studentMail="johndoe@student.university.com"
#)

# Création d'une section et d'une UE
#section = Section.objects.create(wording="Sciences")
#academic_ue = AcademicUE.objects.create(idUE="MATH101", wording="Mathématiques", numberPeriods=30,
                                       # section=section, academicYear="2024-2025", yearCycle=1)

# Création d'une session
#session = Session.objects.create(jour=15, mois=6, academicUE=academic_ue)

# Inscription de l'étudiant à la session avec un statut
#participation = Participation.objects.create(student=student, session=session, status="present")

# Vérifier les participations d'un étudiant
#for p in student.participations.all():
#    print(p)

# Vérifier les participations d'une session
#for p in session.participations.all():
#    print(p)





class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    academic_ue = models.ForeignKey(AcademicUE, on_delete=models.CASCADE, related_name='registrations')
    approved = models.BooleanField(default=False)  # Indique si l'inscription est approuvée
    result = models.FloatField(null=True, blank=True)  # Résultat de l'étudiant (peut être null)
    status = models.CharField(max_length=2, choices=[("NP", "Non Passé"), ("AP", "Approuvé")], default="NP")  # Statut (NP par défaut)

    def __str__(self):
        return f"{self.student} inscrit à {self.academic_ue} - Statut: {self.status}"

#    La classe Registration :

#        student : Une ForeignKey vers le modèle Student, ce qui signifie qu'un étudiant peut avoir plusieurs inscriptions (une par AcademicUE).

#        academic_ue : Une ForeignKey vers le modèle AcademicUE, ce qui signifie qu'une AcademicUE peut avoir plusieurs étudiants inscrits via Registration.

#        approved : Un boolean indiquant si l'inscription a été approuvée.

#        result : Un float pour stocker le résultat de l'étudiant (peut être vide si non noté).

#        status : Un char avec des options "NP" (Non Passé) et "AP" (Approuvé), par défaut "NP".

#    Relation ManyToMany avec la classe Registration :
#    La relation ManyToMany entre Student et AcademicUE est gérée par l'intermédiaire de la classe Registration, ce qui permet d'ajouter des informations supplémentaires (comme le statut ou les résultats).

#Exemple d'utilisation

# Création d'un étudiant
#student = Student.objects.create(
#    first_name="John",
#    last_name="Doe",
#    email="john.doe@example.com",
#    studentMail="johndoe@student.university.com"
#)

# Création d'une section et d'une UE
#section = Section.objects.create(wording="Sciences")
#academic_ue = AcademicUE.objects.create(idUE="MATH101", wording="Mathématiques", numberPeriods=30,
#                                        section=section, academicYear="2024-2025", yearCycle=1)

# Inscrire l'étudiant à l'UE via Registration
#registration = Registration.objects.create(student=student, academic_ue=academic_ue, approved=True, result=15.5, status="AP")

# Vérifier les inscriptions d'un étudiant
#for reg in student.registrations.all():
#    print(reg)

# Vérifier les étudiants inscrits dans une UE
#for reg in academic_ue.registrations.all():
#    print(reg)

#Résultat attendu

#John Doe (johndoe@student.university.com) inscrit à MATH101 - Mathématiques (2024-2025, Cycle 1) - Statut: AP
#John Doe (johndoe@student.university.com) inscrit à MATH101 - Mathématiques (2024-2025, Cycle 1) - Statut: AP