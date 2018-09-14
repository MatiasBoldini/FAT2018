from django.contrib import admin
from .models import *

# normal models
admin.site.register(Person)
admin.site.register(Room)
admin.site.register(Classroom)
admin.site.register(Classroom_day)
admin.site.register(Work_day)
admin.site.register(Appointment)

# request models
admin.site.register(Person_request)