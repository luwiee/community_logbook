from django.contrib import admin
from .models import *
# Register your models here.

class FooAdmin(admin.ModelAdmin):
    readonly_fields = ('time_stamp',)

admin.site.register(log,FooAdmin)
