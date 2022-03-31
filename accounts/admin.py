from django.contrib import admin

# Register your models here.
from accounts.models import homeOwner, house

admin.site.register(homeOwner)
admin.site.register(house)
