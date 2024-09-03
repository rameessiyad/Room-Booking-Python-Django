from django.contrib import admin
from myapp.models import vowner
from myapp.models import staff
from myapp.models import Userreg
from myapp.models import roomtype
from myapp.models import room
from myapp.models import booking
from myapp.models import bsub,temp,temp1

# Register your models here.

admin.site.register(vowner)
admin.site.register(staff)
admin.site.register(Userreg)
admin.site.register(roomtype)
admin.site.register(room)
admin.site.register(booking)
admin.site.register(bsub)
admin.site.register(temp)
admin.site.register(temp1)