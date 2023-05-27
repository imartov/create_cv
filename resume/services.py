# services.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sy_site.settings")
django.setup()

from mysite.resume.models import PersonalData


def get_personal_data():
    list_data = PersonalData.objects.all()
    return list_data
