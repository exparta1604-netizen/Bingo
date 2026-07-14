import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_prueba.settings")
django.setup()
from bingo.models import Bingo
from django.utils import timezone

bingo = Bingo.objects.get(idbingo=4)
bingo.fechaprogramadabingo = timezone.now()
bingo.save()
print("Fecha actualizada a:", bingo.fechaprogramadabingo)