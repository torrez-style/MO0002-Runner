# MO0002-Runner (Maze Runner)

Proyecto del Curso MO-0002 Programación I  
Universidad de Costa Rica - Sede de Occidente

## Descripción

Maze Runner es un juego de laberinto desarrollado en Python usando Pygame. El jugador navega por laberintos, evita enemigos, recolecta obsequios y acumula puntos para alcanzar el salón de la fama.

## Características

- Sistema de juego completo: movimiento, colisiones, puntuación
- IA de enemigos con persecución y colisión
- Salón de la fama con persistencia de puntuaciones
- Panel administrativo: carga de laberintos personalizados
- Sistema de audio con efectos
- Interfaz de menús y HUD informativo

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación rápida
```bash
# Clonar repositorio
git clone https://github.com/torrez-style/MO0002-Runner.git
cd MO0002-Runner

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar juego
python main.py
```

## Cómo Jugar

### Controles
- Flechas del teclado: mover jugador
- ESC: regresar al menú principal
- ENTER: seleccionar opción / reiniciar

### Objetivo
1. Navegar por el laberinto con las flechas
2. Evitar ser capturado por los enemigos
3. Recolectar todas las estrellas para completar
4. Acumular puntos y alcanzar el salón de la fama

## Arquitectura del Proyecto

```
MO0002-Runner/
├── main.py                 # Punto de entrada
├── src/                    # Código fuente principal
│   ├── core/              # Motor del juego
│   ├── entities/          # Jugador, enemigos
│   ├── game_logic/        # Lógica de juego
│   ├── ui/                # Interfaces de usuario
│   ├── world/             # Mundo del juego
│   ├── data/              # Gestión de datos
│   └── audio/             # Sistema de audio
├── assets/                # Recursos del juego
├── tests/                 # Casos de prueba
└── docs/                  # Documentación
```

## Testing

```bash
# Ejecutar todas las pruebas
python -m pytest tests/

# Ejecutar pruebas con cobertura
python -m pytest tests/ --cov=src/
```

## Equipo de Desarrollo

- Wendy Ulate Gutierrez
- Manyel Lizandro Torrez
- Luis Alberto Álvarez Gómez
- Kendall Alvarado Artavia

Profesor Tutor: Lic. Manfred Mejías Acevedo

## Licencia

Proyecto académico para el curso MO-0002 Programación I de la Universidad de Costa Rica.

---

Universidad de Costa Rica - Sede de Occidente  
Segundo Ciclo 2025
