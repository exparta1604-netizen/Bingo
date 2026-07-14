import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_prueba.settings")
django.setup()
from django.contrib.auth.models import User

user = User.objects.get(username="9999999999")
user.email = "playermanual2@test.com"
user.save()
print("Email actualizado:", user.email)