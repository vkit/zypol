from django.contrib import admin

# Register your models here.
from .models import Userprofile, Task
admin.site.register(Userprofile)
admin.site.register(Task)