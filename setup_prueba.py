import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_prueba.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from bingo.models import Jugador, Bingo, PartidaBingo, Carton, CartonPartidaBingo, UnidadMonetaria
from bingo.services import generar_lote_cartones, marcar_casilla_manual

User.objects.filter(username="9999999999").delete()
Jugador.objects.filter(cedulaidentidadjugador="9999999999").delete()

moneda = UnidadMonetaria.objects.create(nombremoneda="Dolares Prueba", tipomoneda="Efectivo", simbolomoneda="$", tasaconversionmoneda=1, estadomoneda=True)
bingo = Bingo.objects.create(idunidadmonetaria=moneda, titulobingo="PRUEBA MANUAL", fechaprogramadabingo=timezone.now() + timedelta(hours=1), tipobingo="Virtual", preciocarton=5, premiomayor=1000, descripcionpremiomayor="Premio", estadobingo="Programado")

cartones = []
for c in generar_lote_cartones(10):
    cartones.append(Carton.objects.create(codigocarton=c["codigo"], matriznumeros=c["matriz"], esmaestro=True))
print("Cartones creados:", [c.codigocarton for c in cartones])

user = User.objects.create_user(username="9999999999", password="test1234")
jugador = Jugador.objects.create(nombresjugador="Prueba", apellidosjugador="Manual", cedulaidentidadjugador="9999999999", aliasjugador="PlayerManual", correojugador="playermanual2@test.com", saldocreditojugador=1000, saldovirtualjugador=500, estadocuentajugador="Activo")

partida = PartidaBingo.objects.create(idbingo=bingo, nombreronda="RONDA MANUAL", modalidad_victoria="Tabla Llena", estadopartida="En Juego", horainicio=timezone.now(), bolascantadas="", ultimabola=0)

carton = cartones[0]
asignacion = CartonPartidaBingo.objects.create(idjugador=jugador, idpartida=partida, idcarton=carton, preciopagado=bingo.preciocarton, fechacompra=timezone.now(), estadocarton="Vendido")

print("--- DATOS PARA PROBAR ---")
print("ID partida:", partida.idpartidabingo)
print("Carton asignado:", carton.codigocarton)
print("Matriz del carton:", carton.matriznumeros)
print("Usuario login: 9999999999 / password: test1234")