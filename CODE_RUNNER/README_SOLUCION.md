# Solución Completa - Maze Runner (MO0002-Runner)

## Descripción del Proyecto

Este es el proyecto **MO0002-Runner**, un juego tipo laberinto desarrollado en Python utilizando Pygame. El proyecto está diseñado con arquitectura Orientada a Objetos y utiliza patrones de diseño como Observer para la gestión de eventos.

## Archivos de Solución

### 1. **SOLUCION_COMPLETA.py**
Documentación exhaustiva del proyecto que incluye:
- Arquitectura del sistema
- Descripción de módulos principales
- Sistema de eventos (Patrón Observer)
- Manejadores de eventos
- Estructura de datos
- Código de integración
- Mejoras y extensiones propuestas
- Guía de testeo y debugging

### 2. **MEJORAS_PROPUESTAS.py**
Ejemplos de código para extender la funcionalidad:

#### Mejora 1: Sistema de Guardado de Partidas
```python
gestor = GestorGuardado()
gestor.guardar_partida(juego, "mi_partida.json")
gestor.cargar_partida(juego, "mi_partida.json")
```

#### Mejora 2: Dificultad Progresiva
```python
velocidad = NivelDificultad.calcular_velocidad_enemigos(nivel_actual)
vidas = NivelDificultad.calcular_vidas_iniciales(nivel_actual)
```

#### Mejora 3: Diferentes Tipos de Enemigos
- Perseguidor: Sigue al jugador inteligentemente
- Patrullero: Patrulla un área
- Aleatorio: Movimiento aleatorio
- Teleportador: Se teletransporta ocasionalmente

#### Mejora 4: Sistema de Logros
```python
gestor_logros = GestorLogros()
gestor_logros.desbloquear_logro("primer_nivel")
```

#### Mejora 5: Sistema de Sonidos
```python
gestor_sonidos = GestorSonidos()
gestor_sonidos.cargar_sonido("colisione", "sonido.wav")
gestor_sonidos.reproducir_sonido("colision")
```

#### Mejora 6: Editor de Laberintos
```python
editor = EditorLaberintos(15, 11)
editor.generar_aleatorio()
editor.exportar_a_json("mi_laberinto.json")
```

## Cómo Ejecutar el Juego

### Requisitos
```bash
pip install pygame
```

### Ejecución
```bash
cd tu_ruta_del_proyecto
python -m CODE_RUNNER.main
```

O directamente:
```bash
python CODE_RUNNER/main.py
```

## Estructura de Datos

### Archivo: `niveles.json`
```json
{
  "niveles": [
    {
      "nombre": "Nivel 1",
      "laberinto": [[1,1,1...], [1,0,0...], ...],
      "vel_enemigos": 14,
      "estrellas": 3,
      "enemigos": 2,
      "powerups": 1,
      "colores": {
        "pared": [100, 100, 100],
        "suelo": [200, 200, 200],
        "enemigo": [220, 50, 50]
      }
    }
  ]
}
```

### Archivo: `puntuaciones.json`
```json
[
  {"nombre": "JUGADOR1", "puntuacion": 250},
  {"nombre": "JUGADOR2", "puntuacion": 180}
]
```

## Módulos Principales

### `juego.py`
Clase principal que orquesta toda la lógica del juego.

**Métodos clave:**
- `__init__()`: Inicializa el juego
- `ejecutar()`: Loop principal
- `_configurar_tablero()`: Centra el laberinto
- `_reiniciar_juego()`: Reinicia nivel actual
- `_avanzar_nivel()`: Pasa al siguiente nivel

### `evento.py`
Sistema de eventos con patrón Observer.

**Eventos:**
- `EventoMoverJugador`: Movimiento
- `EventoRecogerEstrella`: Recolección
- `EventoColisionEnemigo`: Colisión
- `EventoPowerUpAgarrado`: PowerUp
- `EventoSeleccionMenu`: Selección

### `vista.py`
Gestión de gráficos con Pygame.

### `menu.py`
Menú principal del juego.

### `pathfinding.py`
Algoritmo BFS para movimiento de enemigos.

## Controles del Juego

| Tecla | Acción |
|-------|--------|
| Flechas ↑↓←→ | Mover al jugador |
| ESC | Volver al menú |
| ENTER | Reintentar (en Game Over) |

## Potenciadores

- **Invulnerable**: Inmunidad a enemigos por 6 segundos
- **Congelar**: Congela a los enemigos
- **Invisible**: Enemigos no persiguen inteligentemente

## Flujo del Juego

1. **Menú Principal**: Seleccionar "JUEGO"
2. **Jugar**: Recoger estrellas, evitar enemigos
3. **Completar Nivel**: Se recogen todas las estrellas
4. **Game Over**: Se pierden 3 vidas
5. **Hall of Fame**: Ver puntuaciones más altas

## Estados del Juego

- `MENU`: Menú principal
- `JUEGO`: Jugando
- `GAME_OVER`: Fin del juego
- `SALON_DE_LA_FAMA`: Hall de fama
- `ADMINISTRACION`: Cargar nuevos niveles

## Debugging

Si el juego no funciona:

1. Verifica que `niveles.json` existe en `CODE_RUNNER/`
2. Comprueba que pygame está instalado
3. Verifica la ruta de archivos
4. Revisa la consola para mensajes de error

## Mejoras Futuras

- [ ] Guardar y cargar partidas
- [ ] Más tipos de enemigos
- [ ] Animaciones
- [ ] Sonidos y música
- [ ] Sistema de logros
- [ ] Dificultad progresiva
- [ ] Multijugador local
- [ ] Editor de laberintos visual
- [ ] Tutorial interactivo
- [ ] Más potenciadores

## Autor

Desarrollado como proyecto académico de Programación Orientada a Objetos en Python.

---

**Para más información, consulta `SOLUCION_COMPLETA.py` y `MEJORAS_PROPUESTAS.py`**
