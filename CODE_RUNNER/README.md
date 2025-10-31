# Maze-Run

Juego tipo laberinto desarrollado con Python y Pygame. Recolecta todas las estrellas de cada nivel y llega a la salida evitando a los enemigos. Incluye perfiles de jugador, registro de puntuaciones y salón de la fama.

## Requisitos
- Python 3.10+
- Pygame 2.x

Instalación de dependencias:

```bash
pip install pygame
```

## Ejecutar

Ejecutar la aplicación desde la raíz del proyecto:

```bash
python -m CODE_RUNNER.main
```

Si no existe un `main.py`, ejecutar el archivo que inicializa la clase `Juego`:

```bash
python CODE_RUNNER/main.py
```

## Controles
- Flechas: mover al jugador
- Enter: confirmar en menús y reintentar tras Game Over
- Escape: volver al menú

## Objetivo del juego
- Recolectar todas las estrellas del nivel
- Llegar a la salida marcada en la grilla
- Evitar a los enemigos. Si te alcanzan, pierdes una vida
- Al completar todos los niveles sin perder todas las vidas se muestra la pantalla de victoria

## Reglas de avance
- El avance al siguiente nivel requiere:
  - Haber recolectado todas las estrellas
  - Estar parado en la salida
- Intentar salir sin todas las estrellas mostrará un mensaje de aviso

## Potenciadores
- Invulnerable: las colisiones no descuentan vidas durante un tiempo limitado
- Congelar: detiene el movimiento de los enemigos temporalmente
- Invisible: los enemigos dejan de usar pathfinding y se mueven de forma más simple

## Estados del juego
- MENÚ: navegación principal, perfiles, salón y administración
- JUEGO: partida en curso
- SALÓN DE LA FAMA: ranking global de puntuaciones
- GAME OVER: derrota o victoria al finalizar la partida

## Perfiles y puntuaciones
- Archivo `perfiles.json` con lista de perfiles
- Archivo `puntuaciones.json` con historial de partidas
- Al terminar la partida se registra la puntuación del perfil activo
- El salón de la fama muestra el ranking de mejores puntuaciones

## Administración
- Contraseña por defecto: `admin2025` (se puede cambiar con variable de entorno `GAME_ADMIN_PASS`)
- Carga de laberintos desde un archivo JSON válido
- Reinicio del salón de la fama (vaciar puntuaciones)

## Diseño de niveles
- Archivo `CODE_RUNNER/niveles.json`
- Estructura esperada:

```json
{
  "niveles": [
    {
      "nombre": "Tutorial Basico",
      "laberinto": [[...],[...]],
      "vel_enemigos": 18,
      "estrellas": 4,
      "enemigos": 2,
      "powerups": 1,
      "entrada": [x, y],
      "salida": [x, y],
      "colores": { "pared": [r,g,b], "suelo": [r,g,b], "enemigo": [r,g,b] }
    }
  ]
}
```

Notas importantes:
- La matriz `laberinto` usa valores enteros:
  - 1: pared
  - 0: suelo transitable
  - 2: entrada
  - 3: salida
- Los bordes deben ser paredes (1) para evitar salidas del mapa
- Debe existir un camino entre la entrada y la salida

## Estructura del código
- `juego.py`: lógica del juego, bucle principal y estados
- `vista.py`: renderizado con Pygame y modales nativos (input y confirmación)
- `menu.py`: menús y administración usando modales de `vista.py`
- `gestor_perfiles.py`: gestión de perfiles, puntuaciones y rankings
- `salon_de_la_fama.py`: interfaz del salón de la fama (si aplica)
- `constantes.py`: colores, estados, tamaños, valores de juego

## Conocidas y limitaciones
- Puede haber condiciones raras de colisión en mapas muy estrechos; se agregó un chequeo de refuerzo pre-render
- Mezcla de dificultad por nivel puede requerir ajuste fino de `vel_enemigos`, cantidad de enemigos y estrellas
- La gestión de archivos asume rutas locales y carpeta `CODE_RUNNER`

## Licencia
Proyecto educativo/demostrativo. Uso libre con atribución.
