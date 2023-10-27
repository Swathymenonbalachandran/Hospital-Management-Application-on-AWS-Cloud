from django.contrib import admin
# Register your models here.
from .models import Department
from .models import Doctors
from .models import Bookappointment

admin.site.register(Department)
admin.site.register(Doctors)
admin.site.register(Bookappointment)