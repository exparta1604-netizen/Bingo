import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_prueba.settings")
django.setup()
from bingo.models import Bingo, PartidaBingo

ids_a_borrar = [2, 3]
for bid in ids_a_borrar:
    b = Bingo.objects.get(idbingo=bid)
    partidas = PartidaBingo.objects.filter(idbingo=b)
    print(f"Bingo ID {bid}: borrando {partidas.count()} partida(s) asociada(s)")
    partidas.delete()
    print(f"Borrando bingo ID {bid} - {b.titulobingo}")
    b.delete()

print("Listo. Bingos restantes con ese titulo:")
for b in Bingo.objects.filter(titulobingo="PRUEBA MANUAL"):
    print(f"ID: {b.idbingo} | Estado: {b.estadobingo}")