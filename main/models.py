from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

USER_TYPE_CHOICES = (
    (0, 'Jubilado'),
    (1, 'Doctor'),
    (2, 'Profesor'),
    (3, 'Administrador'),
)

DAY_CHOICES = {
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miercoles'),
    (3, 'Jueves'),
    (4, 'Viernes'),
}

class Person(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name="person",
                                related_query_name="person")
    user_type= models.IntegerField(choices=USER_TYPE_CHOICES)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
    
    def get_duties(self):
        results= {}
        results['person']= self
        if self.user_type == 0:
            results['appointmets'] = self.appointments
            results['classrooms'] = self.classrooms
        elif self.user_type == 1:
            results['work_day'] = self.work_days
        elif self.user_type == 2:
            results['classrooms'] = self.classrooms
        elif self.user_type == 3:
            results['persons'] = Person.objects.all()
            results['classrooms'] = Classroom.objects.all()
            results['appointments'] = Appointment.objects.all()
            results['rooms'] = Room.objects.all()
            results['person_requests'] = Person_request.objects.all()
        return results

class Room(models.Model):
    name= models.CharField(max_length=30)
    capacity= models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.name, self.capacity)

class Classroom(models.Model):
    name= models.CharField(max_length=30)
    description= models.CharField(max_length=300)
    members= models.ManyToManyField(Person,
                                    related_name="classrooms",
                                    related_query_name="classroom")
    room= models.ForeignKey(Room,
                            on_delete=models.CASCADE,
                            related_name="classrooms",
                            related_query_name="classroom")

    def __str__(self):
        return "{}".format(self.name)

class Classroom_day(models.Model):
    classroom= models.ForeignKey(Classroom,
                                on_delete=models.CASCADE,
                                related_name="classroom_days",
                                related_query_name="classroom_day")
    day= models.IntegerField(choices=DAY_CHOICES)
    hour= models.TimeField()

    def __str__(self):
        return "{} {}".format(self.day, self.classroom)

class Work_day(models.Model):
    person= models.ForeignKey(Person,
                                on_delete=models.CASCADE,
                                related_name="work_days",
                                related_query_name="work_day")
    day= models.DateField()

    def __str__(self):
        return "{} {}".format(self.person, self.day)

class Appointment(models.Model):
    person= models.ForeignKey(Person,
                                on_delete=models.CASCADE,
                                related_name="appointments",
                                related_query_name="appointment")
    hour= models.TimeField()
    authorized= models.BooleanField(default=False)

    def __str__(self):
        return "{} {} {}".format(self.hour, self.authorized, self.person)

class Person_request(models.Model):
    first_name= models.CharField(max_length=30)
    last_name= models.CharField(max_length=30)
    personal_id= models.CharField(max_length=30)
    password= models.CharField(max_length=30)
    email= models.CharField(max_length=30)

    def approved(self):
        new_user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.personal_id,
            password=self.password,
            email=self.email
        )
        Person.objects.create(user=new_user, user_type=0)
        self.delete()
