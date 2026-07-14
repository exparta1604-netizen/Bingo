import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_prueba.settings")
django.setup()
from bingo.models import PartidaBingo

partida = PartidaBingo.objects.get(idpartidabingo=3)
bingo = partida.idbingo
print("Bingo de la partida 3:", bingo.idbingo, "- estado actual:", bingo.estadobingo)
bingo.estadobingo = "En Curso"
bingo.save()
print("Actualizado a:", bingo.estadobingo)