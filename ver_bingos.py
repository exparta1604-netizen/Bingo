import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_prueba.settings")
django.setup()
from bingo.models import Bingo

for b in Bingo.objects.filter(titulobingo="PRUEBA MANUAL"):
    print(f"ID: {b.idbingo} | Estado: {b.estadobingo} | Fecha creado: {b.fechaprogramadabingo}")