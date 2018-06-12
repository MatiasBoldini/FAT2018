from django.db import models
from django.conf import settings
import datetime
from django.db.models import Q

DAYS_CHOICES = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miercoles'),
    (3, 'Jueves'),
    (4, 'Viernes')
)

class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        abstract = True

class Retired(Person):
    def isAffiliate(self):
        if Affiliate.objects.get(retired=self):
            return True
        return False
    
    def isPartner(self):
        if Partner.objects.get(retired=self):
            return True
        return False
    
    def getEnrrolments(self):
        result = Enrrolment.objects.filter(retired=self)
        if result.count() > 0:
            return result
        return False

    def getAppointments(self):
        result = Appointment.objects.filter(retired=self).filter(Q(workday__day__gte=datetime.date.today()))
        if result.count() > 0:
            return result
        return False
        
class Doctor(Person):
    speciality = models.CharField(max_length=32)
    
    def getDays(self):
        wanted_items = set()
        workdays = self.getAllDays()
        for workday in workdays:
            if workday.day >= datetime.date.today():
                wanted_items.add(workday.pk)
        return WorkDay.objects.filter(pk__in = wanted_items)

    def getAllDays(self):
        results = WorkDay.objects.filter(doctor=self)
        return results

    def daysAvailable(self):
        wanted_items = set()
        workdays = self.getDays()
        for workday in workdays:
            if workday.getAppointments():
                wanted_items.add(workday.pk)
        workdays = WorkDay.objects.filter(pk__in = wanted_items)
        if workdays.count()>0:
            return workdays
        return False
 
class Teacher(Person):
    subject = models.CharField(max_length=32)
    
    def getClassrooms(self):
        my_Classrooms = Classroom.objects.filter(teacher=self)
        return my_Classrooms


class RelationRetired(models.Model):
    number = models.IntegerField()
    retired = models.OneToOneField(Retired, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.number, self.retired)

    class Meta:
        abstract = True

class RelationParticipe(models.Model):
    retired = models.ForeignKey(Retired, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

class WorkDay(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.DateField()

    def getAppointmentsUnfilted(self):
        results = Appointment.objects.filter(workday=self)
        return results

    def getAppointments(self):
        results = self.getAppointmentsUnfilted().filter(workday=self, retired__isnull=True)
        if results.count() > 0:
            return results
        return False  

    def getFillAppointments(self):
        results = self.getAppointmentsUnfilted().filter(workday=self, retired__isnull=False)
        if results.count() > 0:
            return results
        return False  

    def __str__(self):
        return "{}/{}".format(self.day.day, self.day.month)

class Classroom(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    def getStudents(self):
        enrrolments = Enrrolment.objects.filter(classroom=self)
        result = set()
        for enrrolment in enrrolments:
            result.add(enrrolment.retired)
        return result

    def getClassroomDays(self):
        result = ClassroomDay.objects.filter(classroom=self)
        return result

    def __str__(self):
        return "{}".format(self.name)

class ClassroomDay(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day = models.DateField()
    start_hour = models.TimeField()
    

class Affiliate(RelationRetired):
    pass    

class Partner(RelationRetired):
    pass

class Enrrolment(RelationParticipe):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def nextDay(self):
        classroomDays = self.classroom.getClassroomDays()
        for classroomDay in classroomDays:
            if classroomDay.day > datetime.date.today():
                return classroomDay
        return False

    def __str__(self):
        classroomDay = self.nextDay()
        if classroomDay:
            return "{} {}".format(self.classroom.name, classroomDay.day)
        return "{} - {}".format(self.classroom.name, "No hay fechas disponibles")

class Appointment(RelationParticipe):
    workday = models.ForeignKey(WorkDay, on_delete=models.CASCADE)
    timeAttendance = models.TimeField()
    
    def __str__(self):
        return "{}".format(self.timeAttendance)