from django.db import models
from django.conf import settings
import datetime

DAYS_CHOICES = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miercoles'),
    (3, 'Jueves'),
    (4, 'Viernes')
)

USER_TYPE_CHOICES = (
    (0, 'Jubilado'),
    (1, 'Doctor'),
    (2, 'Profesor'),
    (3, 'Administrador')
)


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES)

    def get_duties(self):
        results = {}
        if self.user_type == 0:
            results['appointments'] = Appointment.objects.filter(person=self)
            results['enrolments'] = Enrolment_student.objects.filter(person=self)
        elif self.user_type == 1:
            results['work_days'] = Work_day.objects.filter(doctor=self)
        elif self.user_type == 2:
            results['enrolments'] = Enrolment_teacher.objects.filter(person=self)
        else:
            print("Error: {} has a user type incorrect plase modify it".format(self.user.first_name))
        return results

    def delete_duties(self):
        if self.user_type == 2:
            Enrolment_teacher.objects.filter(person=self).delete()

class Classroom_place(models.Model):
    room = models.IntegerField()
    capacity = models.IntegerField()

class Work_day(models.Model):
    doctor = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.DateField()
    
    def get_appoiment(self, person_fill):
        results = Appointment.objets.filter(workday=self, person__isnull=person_fill)
        return results

    def appointment_available(self):
        availables = self.getappoiment(True).count()
        if availables == 0:
            return False
        return True 

class Appointment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    work_day = models.ForeignKey(Work_day, on_delete=models.CASCADE)
    time_attendance = models.TimeField()
    authorized = models.BooleanField(default=False)

class Classroom(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256)
    duration = models.TimeField()
    
    def get_teachers(self):
        results = Enrolment_teacher.objects.filter(classroom=self)
        return results

    def get_classroom_days(self):
        results = Classroom_day.objects.filter(classroom=self).order_by('day')
        return results
    
    def get_next_day(self):
        classroom_days = self.get_classroom_days()
        for classroom_day in classroom_days:
            if classroom_day.day >= datetime.datetime.today().weekday():
                return classroom_day
        return classroom_days.first()

    def get_students(self):
        results = Enrolment_student.objects.filter(classroom=self)
        return results

class Classroom_day(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    classroom_place = models.ForeignKey(Classroom_place, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_CHOICES)
    start_hour = models.TimeField()

class Enrolment_teacher(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

class Enrolment_student(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

# request (necesitan autorizarse por el admin)

class Person_request(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES)

class Classroom_request(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256)
    duration = models.TimeField()
    teacher = models.ForeignKey(Person, on_delete=models.CASCADE)

    def get_days(self):
        results = Classroom_day_request.objects.filter(classroom=self)
        return results

class Classroom_day_request(models.Model):
    classroom = models.ForeignKey(Classroom_request, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_CHOICES)
    start_hour = models.TimeField()

class Enrolment_teacher_request(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

class Enrolment_student_request(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Work_day_request(models.Model):
    start_hour = models.TimeField()
    finish_hour = models.TimeField()
    duration = models.TimeField()
    interval = models.TimeField()
    doctor = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.DateField()

# records (clases sin uso cotidiano)

class Person_record(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=20)
    personal_id = models.IntegerField()
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES)

class Work_day_record(models.Model):
    doctor = models.ForeignKey(Person_record, on_delete=models.CASCADE)
    day = models.DateField()

class Appointment_record(models.Model):
    person = models.ForeignKey(Person_record, on_delete=models.CASCADE)
    work_day = models.ForeignKey(Work_day_record, on_delete=models.CASCADE)
    time_attendance = models.TimeField()

class Classroom_record(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256)

class Classroom_day_record(models.Model):
    classroom = models.ForeignKey(Classroom_record, on_delete=models.CASCADE)
    day = models.IntegerField()
    start_hour = models.TimeField()

class Enrolment_teacher_record(models.Model):
    classroom = models.ForeignKey(Classroom_record, on_delete=models.CASCADE)
    person = models.OneToOneField(Person_record, on_delete=models.CASCADE)

class Enrolment_student_record(models.Model):
    classroom = models.ForeignKey(Classroom_record, on_delete=models.CASCADE)
    person = models.ForeignKey(Person_record, on_delete=models.CASCADE)

class Notification(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    message = models.TextField(max_length=256)