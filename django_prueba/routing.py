from django.urls import re_path
from bingo import consumers 

websocket_urlpatterns = [
  # Captura el ID de la partida directamente desde la URL del WebSocket
  re_path(r'ws/juego/(?P<id_partida>\w+)/$', consumers.BingoConsumer.as_asgi()),
  # FIX: la tienda de cartones abre /ws/tienda/<id_bingo>/ y esta ruta no existía,
  # por lo que las alertas de "cartón vendido" en tiempo real nunca llegaban.
  re_path(r'ws/tienda/(?P<id_bingo>\w+)/$', consumers.TiendaConsumer.as_asgi()),
]
