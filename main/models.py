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

USER_CHOICES = (
    (0, 'jubilado'),
    (1, 'doctor'),
    (2, 'profesor'),
    (3, 'administrador'),
)
class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_CHOICES)

    def get_duties(self):
        if self.user_type == 0:
            result = None
        elif self.user_type == 1:
            result = Work_day.objects.filter(doctor=self)
        elif self.user_type == 2:
            result = Enrolment_teacher.objects.filter(person=self)
        elif self.user_type == 3:
            result = None
        else:
            result = None
            print("Error: {} has a user type incorrect plase modify it".format(user.first_name))
        return result

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

class Classroom(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256)
    duration = models.TimeField()
    
    def get_classroom_days(self):
        results = Classroom_day.objects.filter(classroom=self).order_by('day')
        print(results)
        return results

    def get_classroom_place(self):
        result = Classroom_place.objects.get(classroom=self)
        return result
    
    def get_next_day(self):
        classroom_days = self.get_classroom_days()
        for classroom_day in classroom_days:
            if classroom_day.day >= datetime.datetime.today().weekday():
                return classroom_day
        return classroom_days.first()


class Classroom_day(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_CHOICES)
    start_hour = models.TimeField()

class Classroom_place(models.Model):
    room = models.IntegerField()
    capacity = models.IntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

class Appointment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    work_day = models.ForeignKey(Work_day, on_delete=models.CASCADE)
    time_attendance = models.TimeField()
    authorized = models.BooleanField(default=False)

class Enrolment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Enrolment_teacher(Enrolment):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)


class Enrolment_student(Enrolment):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)