from django.contrib import admin
from .models import TipoSocio, Socio, Prestamo, Pago, MetodoPago, Regalo
from .models import AporteSemanal, CuentaBancaria, Ahorro, Bingo, PartidaBingo
from .models import CartonPartidaBingo, Carton, Jugador, SesionJuego, PlataformaJuego, UnidadMonetaria, ConfiguracionWeb, MensajeChat

# Personalización del sitio de administración
admin.site.site_header = "CoopBingo — Administración"
admin.site.site_title = "CoopBingo Admin"
admin.site.index_title = "Panel de gestión de la cooperativa"


@admin.register(TipoSocio)
class TipoSocioAdmin(admin.ModelAdmin):
    list_display = ('nombretiposocio', 'roltiposocio', 'descripciondetiposocio')
    search_fields = ('nombretiposocio', 'roltiposocio')


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ('cisocio', 'primernombresocio', 'primerapellidosocio', 'telefonopersonalsocio', 'idtiposocio', 'estadosocio')
    list_filter = ('estadosocio', 'idtiposocio', 'sexosocio')
    search_fields = ('cisocio', 'primernombresocio', 'primerapellidosocio')
    list_per_page = 50


@admin.register(CuentaBancaria)
class CuentaBancariaAdmin(admin.ModelAdmin):
    list_display = ('numerocuenta', 'nombrebanco', 'idsocio', 'tipocuenta', 'esprincipal', 'estadocuenta')
    list_filter = ('nombrebanco', 'tipocuenta', 'estadocuenta', 'esprincipal')
    search_fields = ('numerocuenta', 'idsocio__cisocio', 'idsocio__primerapellidosocio')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('idprestamo', 'idsocio', 'montoprestamosolicitado', 'saldopendiente', 'numerocuotas', 'fechavencimiento', 'estadoprestamo')
    list_filter = ('estadoprestamo',)
    search_fields = ('idsocio__cisocio', 'idsocio__primerapellidosocio')
    date_hierarchy = 'fechasolicitud'


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('idpago', 'idprestamo', 'montopagado', 'idmetodopago', 'fechapago', 'estadopago')
    list_filter = ('estadopago', 'idmetodopago')
    search_fields = ('numeroreferencia', 'idprestamo__idsocio__cisocio')
    date_hierarchy = 'fechapago'


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('nombremetodopago', 'estadometodopago', 'urlmetodopago')
    list_filter = ('estadometodopago',)
    search_fields = ('nombremetodopago',)


@admin.register(Regalo)
class RegaloAdmin(admin.ModelAdmin):
    list_display = ('nombreregalo', 'valorregalo', 'estadoregalo', 'fechaentregaregalo')
    list_filter = ('estadoregalo',)
    search_fields = ('nombreregalo',)


@admin.register(AporteSemanal)
class AporteSemanalAdmin(admin.ModelAdmin):
    list_display = ('idaporte', 'idsocio', 'numerosemana', 'fechaplanificadadada', 'metodoingreso', 'estadoaporte')
    list_filter = ('estadoaporte', 'metodoingreso')
    search_fields = ('idsocio__cisocio', 'idsocio__primerapellidosocio')


@admin.register(Ahorro)
class AhorroAdmin(admin.ModelAdmin):
    list_display = ('idahorro', 'idsocio', 'tipoahorro', 'montoahorro', 'fechaahorro', 'estadoahorro')
    list_filter = ('tipoahorro', 'estadoahorro')
    search_fields = ('idsocio__cisocio', 'idsocio__primerapellidosocio')
    date_hierarchy = 'fechaahorro'


@admin.register(Bingo)
class BingoAdmin(admin.ModelAdmin):
    list_display = ('idbingo', 'titulobingo', 'fechaprogramadabingo', 'tipobingo', 'preciocarton', 'premiomayor', 'estadobingo')
    list_filter = ('estadobingo', 'tipobingo')
    search_fields = ('titulobingo',)
    date_hierarchy = 'fechaprogramadabingo'


@admin.register(PartidaBingo)
class PartidaBingoAdmin(admin.ModelAdmin):
    list_display = ('idpartidabingo', 'idbingo', 'nombreronda', 'modalidad_victoria', 'valorpremio', 'estadopartida', 'ultimabola')
    list_filter = ('estadopartida', 'modalidad_victoria')
    search_fields = ('nombreronda', 'idbingo__titulobingo')


@admin.register(Carton)
class CartonAdmin(admin.ModelAdmin):
    list_display = ('codigocarton', 'esmaestro', 'indicevictoria')
    list_filter = ('esmaestro',)
    search_fields = ('codigocarton',)
    list_per_page = 50


@admin.register(CartonPartidaBingo)
class CartonPartidaBingoAdmin(admin.ModelAdmin):
    list_display = ('idcartonpartida', 'idcarton', 'idpartida', 'idjugador', 'preciopagado', 'estadocarton', 'esganador')
    list_filter = ('estadocarton', 'esganador')
    search_fields = ('idcarton__codigocarton', 'idjugador__aliasjugador', 'idjugador__cedulaidentidadjugador')
    list_per_page = 50


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('aliasjugador', 'cedulaidentidadjugador', 'correojugador', 'saldocreditojugador', 'saldovirtualjugador', 'estadocuentajugador', 'idsocio')
    list_filter = ('estadocuentajugador',)
    search_fields = ('aliasjugador', 'cedulaidentidadjugador', 'correojugador')
    list_per_page = 50


@admin.register(SesionJuego)
class SesionJuegoAdmin(admin.ModelAdmin):
    list_display = ('idsesion', 'idjugador', 'idpartida', 'fechainiciosesion', 'estadosesion', 'dispositivoconexion', 'ipconexion')
    list_filter = ('estadosesion', 'dispositivoconexion')
    search_fields = ('idjugador__aliasjugador',)
    date_hierarchy = 'fechainiciosesion'


@admin.register(PlataformaJuego)
class PlataformaJuegoAdmin(admin.ModelAdmin):
    list_display = ('nombreplataforma', 'urlplataforma', 'estadoplataforma', 'fechavencimientolicencia')
    list_filter = ('estadoplataforma',)
    search_fields = ('nombreplataforma',)


@admin.register(UnidadMonetaria)
class UnidadMonetariaAdmin(admin.ModelAdmin):
    list_display = ('nombremoneda', 'simbolomoneda', 'tipomoneda', 'tasaconversionmoneda', 'estadomoneda')
    list_filter = ('tipomoneda', 'estadomoneda')
    search_fields = ('nombremoneda',)


@admin.register(ConfiguracionWeb)
class ConfiguracionWebAdmin(admin.ModelAdmin):
    list_display = ('idconfiguracion', 'titulosobrenosotros', 'numerowhatsapp', 'fechaultimaactualizacion')


@admin.register(MensajeChat)
class MensajeChatAdmin(admin.ModelAdmin):
    list_display = ('idmensaje', 'idbingo', 'usuario', 'mensaje', 'fechahora')
    list_filter = ('idbingo',)
    search_fields = ('usuario', 'mensaje')
    date_hierarchy = 'fechahora'
    readonly_fields = ('fechahora',)
