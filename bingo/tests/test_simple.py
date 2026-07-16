# bingo/tests/test_simple.py
import json
import random
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from bingo.models import (
    TipoSocio, Jugador, Bingo, PartidaBingo, 
    Carton, CartonPartidaBingo, UnidadMonetaria, SesionJuego, PlataformaJuego
)
from bingo.services import (
    generar_lote_cartones, 
    auditar_patron_bingo,
    marcar_casilla_manual
)

class BingoGameTest(TestCase):
    """Suite completa de pruebas para el Bingo en juego - Versión Corregida"""

    def setUp(self):
        print("\n" + "="*80)
        print("[SETUP] PREPARANDO ESCENARIO DE PRUEBA")
        print("="*80)
        
        # 1. Tipo de Socio
        self.tipo_socio, _ = TipoSocio.objects.get_or_create(
            nombretiposocio='Socio Activo',
            defaults={
                'roltiposocio': 'miembro',
                'descripciondetiposocio': 'Socio regular de la cooperativa'
            }
        )
        
        # 2. Moneda
        self.moneda = UnidadMonetaria.objects.create(
            nombremoneda='Dólares',
            tipomoneda='Efectivo',
            simbolomoneda='$',
            tasaconversionmoneda=1.00,
            estadomoneda=True
        )
        
        # 3. Admin
        self.admin = User.objects.create_user(
            username='admin123',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        
        # 4. Jugadores
        self.jugadores = []
        for i in range(3):
            cedula = f'100000000{i}'
            user = User.objects.create_user(
                username=cedula,
                email=f'jugador{i}@test.com',
                password='testpass123'
            )
            jugador = Jugador.objects.create(
                nombresjugador=f'Jugador {i}',
                apellidosjugador=f'Apellido{i}',
                cedulaidentidadjugador=cedula,
                aliasjugador=f'Player{i}',
                correojugador=f'jugador{i}@test.com',
                saldocreditojugador=5000.00,
                saldovirtualjugador=1000.00,
                estadocuentajugador='Activo'
            )
            self.jugadores.append(jugador)
        
        # 5. Bingo
        self.bingo = Bingo.objects.create(
            idunidadmonetaria=self.moneda,
            titulobingo='BINGO PRUEBA COMPLETA',
            fechaprogramadabingo=timezone.now() + timedelta(hours=1),
            tipobingo='Virtual',
            preciocarton=5.00,
            premiomayor=1000.00,
            descripcionpremiomayor='Gran Premio',
            estadobingo='Programado'
        )
        
        # 6. Cartones
        lote = generar_lote_cartones(10)
        self.cartones = []
        for c in lote:
            carton = Carton.objects.create(
                codigocarton=c['codigo'],
                matriznumeros=c['matriz'],
                esmaestro=True
            )
            self.cartones.append(carton)
        
        # 7. Plataforma
        self.plataforma, _ = PlataformaJuego.objects.get_or_create(
            nombreplataforma='Web Oficial',
            defaults={'urlplataforma': 'http://localhost:8000/', 'estadoplataforma': True}
        )
        
        print("[OK] Escenario preparado correctamente")
        print("="*80 + "\n")

    # ==================== TESTS CORREGIDOS ====================

    def test_01_crear_partida(self):
        print("\n[TEST 1] Crear Partida")
        partida = PartidaBingo.objects.create(
            idbingo=self.bingo,
            nombreronda='RONDA 1',
            modalidad_victoria='Tabla Llena',
            valorpremio=100.00,
            premiomaterial='Ninguno',
            estadopartida='Programada',
            bolascantadas='',
            ultimabola=0
        )
        self.assertEqual(partida.estadopartida, 'Programada')
        print(f"[OK] Partida creada: {partida.nombreronda}")

    def test_02_compra_cartones(self):
        print("\n[TEST 2] Compra de Cartones")
        partida = PartidaBingo.objects.create(
            idbingo=self.bingo,
            nombreronda='RONDA COMPRA',
            modalidad_victoria='Tabla Llena',
            estadopartida='Programada',
            bolascantadas='',
            ultimabola=0
        )
        for i, jugador in enumerate(self.jugadores):
            carton = self.cartones[i]
            saldo_inicial = jugador.saldocreditojugador
            CartonPartidaBingo.objects.create(
                idjugador=jugador,
                idpartida=partida,
                idcarton=carton,
                preciopagado=self.bingo.preciocarton,
                fechacompra=timezone.now(),
                estadocarton='Vendido'
            )
            jugador.saldocreditojugador -= self.bingo.preciocarton
            jugador.save()
            print(f"[OK] {jugador.aliasjugador} compró cartón {carton.codigocarton}")

    def test_03_iniciar_partida(self):
        print("\n[TEST 3] Iniciar Partida")
        partida = PartidaBingo.objects.create(
            idbingo=self.bingo,
            nombreronda='RONDA INICIO',
            modalidad_victoria='Tabla Llena',
            estadopartida='Programada',
            bolascantadas='',
            ultimabola=0
        )
        partida.estadopartida = 'En Juego'
        partida.horainicio = timezone.now()
        partida.save()
        self.bingo.estadobingo = 'En Curso'
        self.bingo.save()
        print(f"[OK] Partida iniciada correctamente")

    def test_04_sistema_bolas(self):
        print("\n[TEST 4] Sistema de Bolas")
        partida = PartidaBingo.objects.create(
            idbingo=self.bingo,
            nombreronda='RONDA BOLAS',
            modalidad_victoria='Tabla Llena',
            estadopartida='En Juego',
            horainicio=timezone.now(),
            bolascantadas='',
            ultimabola=0
        )
        bolas_extraidas = []
        for _ in range(20):
            bolas_str = partida.bolascantadas.replace('B','').replace('I','').replace('N','').replace('G','').replace('O','')
            bolas_llamadas = [int(b.strip()) for b in bolas_str.split(',') if b.strip().isdigit()]
            bolas_disponibles = [i for i in range(1, 76) if i not in bolas_llamadas]
            if not bolas_disponibles: break
            nueva_bola = random.choice(bolas_disponibles)
            bolas_llamadas.append(nueva_bola)
            bolas_extraidas.append(nueva_bola)
            partida.ultimabola = nueva_bola
            partida.bolascantadas = ",".join(map(str, bolas_llamadas))
            partida.save()
        self.assertEqual(len(set(bolas_extraidas)), len(bolas_extraidas))
        print(f"[OK] Se extrajeron {len(bolas_extraidas)} bolas sin duplicados")

    def test_05_marcar_numeros(self):
        print("\n[TEST 5] Marcar Números (Corregido)")
        partida = PartidaBingo.objects.create(
            idbingo=self.bingo,
            nombreronda='RONDA MARCADO',
            modalidad_victoria='Tabla Llena',
            estadopartida='En Juego',
            bolascantadas='',
            ultimabola=0
        )
        jugador = self.jugadores[0]
        carton = self.cartones[0]
        
        # Extraer números reales del cartón para evitar errores
        matriz = carton.matriznumeros
        numeros_reales = []
        for col in ['B', 'I', 'N', 'G', 'O']:
            for num in matriz[col]:
                if num != "FREE":
                    numeros_reales.append(num)
        
        # FIX: seleccionamos los números que vamos a marcar y los
        # "cantamos" en la partida ANTES de intentar marcarlos, ya que
        # marcar_casilla_manual exige que el número ya haya salido.
        numeros_a_marcar = numeros_reales[:8]  # Marcamos 8 números seguros
        partida.bolascantadas = ",".join(map(str, numeros_a_marcar))
        partida.save()
        
        SesionJuego.objects.create(
            idplataforma=self.plataforma,
            idjugador=jugador,
            idpartida=partida,
            fechainiciosesion=timezone.now(),
            estadosesion='Activa',
            tokenconexion='test-token-123'
        )
        
        asignacion = CartonPartidaBingo.objects.create(
            idjugador=jugador,
            idpartida=partida,
            idcarton=carton,
            estadocarton='Vendido'
        )
        
        # Marcar solo números que realmente existen en el cartón Y que ya fueron cantados
        for numero in numeros_a_marcar:
            resultado = marcar_casilla_manual(
                jugador.idjugador, carton.codigocarton, numero, partida.idpartidabingo
            )
            self.assertTrue(resultado, f"No se pudo marcar el número {numero}")
        
        asignacion.refresh_from_db()
        print(f"[OK] Se marcaron {asignacion.cantidadaciertos} números correctamente")

    def test_06_patrones_bingo(self):
        print("\n[TEST 6] Patrones de Victoria (Corregido)")
        matriz = {
            'B': [1, 2, 3, 4, 5],
            'I': [16, 17, 18, 19, 20],
            'N': [31, 32, "FREE", 34, 35],
            'G': [46, 47, 48, 49, 50],
            'O': [61, 62, 63, 64, 65]
        }
        bolas = [1,2,3,4,5,16,17,18,19,20,31,32,34,35,46,47,48,49,50,61,62,63,64,65]
        
        self.assertTrue(auditar_patron_bingo(matriz, bolas, 'Tabla Llena'))
        self.assertTrue(auditar_patron_bingo(matriz, [1,5,31,35,61,65], 'Las Cuatro Esquinas'))
        # FIX: "Linea Vertical" = una columna completa (ej. columna B: 1,2,3,4,5),
        # no un número de cada columna (eso sería una fila/horizontal).
        self.assertTrue(auditar_patron_bingo(matriz, [1,2,3,4,5], 'Linea Vertical'))
        self.assertTrue(auditar_patron_bingo(matriz, [1,17,"FREE",49,65], 'En Diagonal'))
        print("[OK] Todos los patrones detectados correctamente")

    def test_07_finalizar_y_premio(self):
        print("\n[TEST 7] Finalizar y Asignar Premio")
        partida = PartidaBingo.objects.create(
            idbingo=self.bingo,
            nombreronda='RONDA FINAL',
            modalidad_victoria='Tabla Llena',
            estadopartida='En Juego',
            valorpremio=200.00,
            bolascantadas='',
            ultimabola=0
        )
        jugador = self.jugadores[0]
        saldo_inicial = jugador.saldocreditojugador
        
        partida.idjugadororganador = jugador
        partida.estadopartida = 'Finalizada'
        partida.horafin = timezone.now()
        partida.save()
        
        jugador.saldocreditojugador += partida.valorpremio
        jugador.save()
        
        print(f"[OK] Premio de ${partida.valorpremio} asignado correctamente")
        self.assertGreater(jugador.saldocreditojugador, saldo_inicial)

    def test_08_desempate(self):
        print("\n[TEST 8] Desempate")
        partida = PartidaBingo.objects.create(
            idbingo=self.bingo,
            nombreronda='RONDA DESEMPATE',
            modalidad_victoria='Tabla Llena',
            estadopartida='Desempate',
            idbingadores=f'{self.jugadores[0].idjugador},{self.jugadores[1].idjugador}',
            valorpremio=500.00,
            bolascantadas='',
            ultimabola=0
        )
        sorteo = {
            str(self.jugadores[0].idjugador): 45,
            str(self.jugadores[1].idjugador): 72
        }
        partida.sorteodesempate = sorteo
        ganador_id = max(sorteo, key=sorteo.get)
        partida.idjugadororganador_id = int(ganador_id)
        partida.estadopartida = 'Finalizada'
        partida.horafin = timezone.now()
        partida.save()
        
        print(f"[OK] Desempate resuelto correctamente - Ganador ID: {ganador_id}")

    def test_09_multiples_rondas(self):
        print("\n[TEST 9] Múltiples Rondas")
        for i in range(3):
            ronda = PartidaBingo.objects.create(
                idbingo=self.bingo,
                nombreronda=f'RONDA {i+1}',
                modalidad_victoria='Tabla Llena',
                estadopartida='Programada',
                bolascantadas='',
                ultimabola=0
            )
            ronda.estadopartida = 'En Juego'
            ronda.horainicio = timezone.now()
            ronda.save()
            
            # Extraer algunas bolas
            for _ in range(5):
                bolas_str = ronda.bolascantadas.replace('B','').replace('I','').replace('N','').replace('G','').replace('O','')
                bolas_llamadas = [int(b.strip()) for b in bolas_str.split(',') if b.strip().isdigit()]
                disponibles = [x for x in range(1, 76) if x not in bolas_llamadas]
                if disponibles:
                    nueva = random.choice(disponibles)
                    bolas_llamadas.append(nueva)
                    ronda.ultimabola = nueva
                    ronda.bolascantadas = ",".join(map(str, bolas_llamadas))
                    ronda.save()
            
            ronda.idjugadororganador = self.jugadores[i % 3]
            ronda.estadopartida = 'Finalizada'
            ronda.horafin = timezone.now()
            ronda.save()
            print(f"[OK] Ronda {i+1} finalizada")
        
        self.bingo.estadobingo = 'Finalizado'
        self.bingo.save()
        print("[OK] Bingo completado con múltiples rondas")