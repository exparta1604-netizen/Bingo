# 🎱 CoopBingo — Plataforma de Bingo Cooperativo en Tiempo Real

Sistema web desarrollado en **Django 6** para la gestión integral de una cooperativa que organiza bingos: socios, jugadores, préstamos, ahorros, aportes semanales y partidas de bingo **en vivo** con WebSockets.

## ✨ Funcionalidades

### Para jugadores
- Registro como **jugador** (solo juega) o **socio** (miembro de la cooperativa con acceso a préstamos y ahorros), con posibilidad de "ascender" de jugador a socio desde el perfil.
- **Tienda de cartones**: compra de cartones del catálogo maestro o generados al momento, con saldo virtual/real y avisos en tiempo real cuando otro jugador compra un cartón (límite de 15 cartones por evento).
- **Sala de espera y tablero en vivo**: bolas cantadas por WebSocket, marcado manual de casillas validado en el servidor, chat en vivo y lista de jugadores conectados.
- **Desempates**: sala VIP para finalistas con sorteo de bola mayor.
- Descarga de cartones en **PDF** para jugar de forma presencial o por Zoom.
- Perfil con historial de compras, préstamos y ahorros, cambio de avatar y contraseña.

### Para administradores
- **Dashboard SPA** con estadísticas (socios, jugadores, ganancias por día/semana/mes/año), gestión de bingos, rondas, monedas, plataformas, tipos de socio y configuración del sitio.
- **Consola de juego en vivo**: sorteo de bolas con RNG criptográfico, radar de ganadores en tiempo real, verificación híbrida de cartones (jugadores web vs. externos), gestión de desempates y pago automático de premios.
- **Reportes**: liquidación por bingo (Excel), cartera de préstamos (Excel), socios puntuales (Excel) y cierre de caja semanal (PDF).
- **Django Admin** configurado con búsqueda, filtros y columnas para todos los modelos.

## 🛠️ Stack tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Django 6.0 (Python 3.12+) |
| Tiempo real | Django Channels 4 + Daphne (ASGI) |
| Capa de canales | Redis (o memoria en desarrollo) |
| Tareas en segundo plano | Celery + Redis |
| Base de datos | SQLite (desarrollo) |
| Reportes | openpyxl (Excel), xhtml2pdf (PDF) |
| Frontend | Plantillas Django + Bootstrap 5 + JS vanilla |

## 🚀 Instalación y ejecución

### 1. Clonar e instalar dependencias

```bash
git clone https://github.com/exparta1604-netizen/Bingo.git
cd Bingo
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno (opcional en desarrollo)

El proyecto arranca sin configuración extra. Para personalizar, revisa [.env.example](.env.example):

| Variable | Descripción | Por defecto |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta (obligatoria en producción) | clave de desarrollo |
| `DJANGO_DEBUG` | Modo debug | `true` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por coma | `localhost,127.0.0.1` |
| `DJANGO_USE_REDIS` | `false` = WebSockets en memoria (sin Redis) | `true` |
| `REDIS_HOST` / `REDIS_PORT` | Servidor Redis | `127.0.0.1:6379` |

### 3. Migrar la base de datos y crear el administrador

```bash
python manage.py migrate
python manage.py createsuperuser
```

> **Importante:** crea al menos un registro de **Tipo de Socio** y una **Unidad Monetaria** desde `/admin/` antes de registrar socios o crear bingos.

### 4. Levantar los servicios

```bash
# Sin Redis instalado (desarrollo rápido, un solo proceso):
# Windows PowerShell:  $env:DJANGO_USE_REDIS = "false"
# Linux/Mac:           export DJANGO_USE_REDIS=false
python manage.py runserver
```

Con Redis y Celery (recomendado, experiencia completa):

```bash
# Terminal 1 — Redis (instalado o vía Docker)
docker run -p 6379:6379 redis

# Terminal 2 — Celery (fábrica de cartones en segundo plano)
celery -A django_prueba worker -l info

# Terminal 3 — Servidor web con WebSockets
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/>

### 5. Ejecutar los tests

```bash
python manage.py test bingo
```

## 📂 Estructura del proyecto

```
Bingo/
├── django_prueba/          # Configuración del proyecto
│   ├── settings.py         # Ajustes (endurecidos con variables de entorno)
│   ├── urls.py             # Rutas HTTP
│   ├── routing.py          # Rutas WebSocket (juego y tienda)
│   ├── asgi.py             # Aplicación ASGI (Daphne)
│   └── celery.py           # Configuración de Celery
├── bingo/                  # Aplicación principal
│   ├── models.py           # 18 modelos (Socio, Jugador, Bingo, Partida, Cartón...)
│   ├── views.py            # Vistas: públicas, cuentas, dashboard, juego en vivo
│   ├── services.py         # Lógica de negocio: RNG de cartones, árbitro digital
│   ├── consumers.py        # WebSockets: partida en vivo y tienda
│   ├── tasks.py            # Tareas Celery
│   ├── admin.py            # Django Admin configurado
│   ├── templates/          # Plantillas (comunes, cuentas, administrador, partida...)
│   ├── static/             # CSS y JS (incluye motor de sockets del cliente)
│   └── tests/              # Suite de pruebas (9 tests del flujo de juego)
├── docs/                   # Documentación técnica (Word)
├── requirements.txt        # Dependencias
└── .env.example            # Plantilla de variables de entorno
```

## 🔒 Seguridad

Medidas implementadas en la revisión de seguridad del proyecto:

- **Secretos fuera del código**: `SECRET_KEY`, `DEBUG` y hosts se leen de variables de entorno; la base de datos y archivos subidos ya no se versionan en Git.
- **Anti XSS**: todo dato de usuario (chat, alias) se escapa antes de insertarse en el DOM; los mensajes de chat se validan y truncan también en el servidor.
- **Anti fuerza bruta**: el login bloquea 5 intentos fallidos por identificador/IP durante 5 minutos.
- **Contraseñas robustas**: los registros y cambios de clave validan contra las reglas de Django (mínimo 8 caracteres, no comunes, no solo números).
- **Transacciones atómicas con bloqueo de fila** en la compra de cartones (evita dobles compras y saldos negativos) y en los registros de usuarios.
- **Validación del lado del servidor de los cartones generados en el navegador** (estructura, rangos B-I-N-G-O, sin duplicados): un cliente malicioso no puede inyectar cartones inventados.
- **RNG criptográfico** (`secrets`) para el sorteo de bolas.
- **Cabeceras y cookies seguras**: HSTS, redirección SSL, cookies `Secure`/`HttpOnly`, `X-Frame-Options: DENY` (activas en producción con `DJANGO_DEBUG=false`).
- **Límite de subida de archivos** (5 MB) y expiración de sesión a las 8 horas.

## 📖 Documentación

La documentación técnica completa (arquitectura, modelo de datos, manual de usuario y administrador, y detalle de la auditoría de mejoras) está en [docs/Documentacion_CoopBingo.docx](docs/Documentacion_CoopBingo.docx).

## 👥 Créditos

Proyecto colaborativo académico. Mejoras de seguridad, corrección de errores y documentación por **Jean Arauz**.
