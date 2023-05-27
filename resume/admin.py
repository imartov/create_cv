from django.contrib import admin

from .models import *

admin.site.register(PersonalData)
admin.site.register(Skills)
admin.site.register(WorkExperience)
# admin.site.register(Responsibilities)
# admin.site.register(Progress)
admin.site.register(References)
admin.site.register(Contacts)
admin.site.register(Position)