# Maze-Run (estructura refactorizada)

Juego tipo laberinto desarrollado con Python y Pygame. Recolecta todas las estrellas y llega a la salida evitando a los enemigos. Ahora organizado bajo `src/` sin cambiar la lógica.

## Requisitos
- Python 3.10+
- Pygame 2.x

Instalar dependencias:

```bash
pip install pygame
```

## Cómo ejecutar
Opciones:

- Desde la raíz del repo (recomendado):

```bash
python main.py
```

- O como módulo usando el paquete `src`:

```bash
python -m src.juego.juego
```

- También se mantiene un shim para compatibilidad:

```bash
python CODE_RUNNER/main.py
```

## Estructura

```
src/
  clases/
    enemigo.py
    jugador.py
    personaje.py
    puntuacion.py
  juego/
    __init__.py
    constantes.py
    evento.py
    gestor_perfiles.py
    juego.py
    menu.py
    pathfinding.py
    salon_de_la_fama.py
    vista.py
  data/
    niveles.json
    perfiles.json
    puntuaciones.json
  test/
```

## Datos y administración
- Los archivos de datos ahora viven en `src/data/`.
- En el menú de Administración puedes cargar nuevos laberintos; se guardan en `src/data/niveles.json`.
- El reinicio del salón de la fama limpia `src/data/puntuaciones.json`.

## Controles
- Flechas: mover
- Enter: confirmar / reintentar
- Escape: volver

## Notas
- Si tenías archivos JSON previos en `CODE_RUNNER/`, se han copiado a `src/data/`.
- Pygame debe estar instalado en el entorno activo.
