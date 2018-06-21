from django.db import models
from django.conf import settings
import datetime


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.IntegerField()

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
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    work_day = models.ForeignKey(Work_day, on_delete=models.CASCADE)
    time_attendance = models.TimeField()

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
    day = models.IntegerField()
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
    user_type = models.IntegerField()

class Classroom_request(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256)
    duration = models.TimeField()
    user = models.ForeignKey(Person, on_delete=models.CASCADE)

class Classroom_day_request(models.Model):
    classroom = models.ForeignKey(Classroom_request, on_delete=models.CASCADE)
    day = models.IntegerField()
    start_hour = models.TimeField()

class Enrolment_teacher_request(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

class Enrolment_student_request(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Work_day_request(models.Model):
    doctor = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.DateField()

class Appointment_request(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    work_day = models.ForeignKey(Work_day, on_delete=models.CASCADE)
    time_attendance = models.TimeField()

# records (clases sin uso cotidiano)

class Person_record(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=20)
    personal_id = models.IntegerField()
    user_type = models.IntegerField()

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