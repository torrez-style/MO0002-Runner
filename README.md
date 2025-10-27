# 🎮 MO0002-Runner (Maze Runner)

**Proyecto del Curso MO-0002 Programación I**  
Universidad de Costa Rica - Sede de Occidente

## 📖 Descripción

Maze Runner es un juego de laberinto desarrollado en Python usando Pygame. El jugador debe navegar por laberintos mientras evita enemigos inteligentes, recolecta obsequios y acumula puntos para alcanzar el salón de la fama.

## ✨ Características

- 🎯 **Sistema de juego completo**: Movimiento, colisiones, puntuación
- 🤖 **IA inteligente**: Enemigos con pathfinding algoritmo BFS
- 🏆 **Salón de la fama**: Persistencia de mejores puntuaciones
- 🔧 **Panel administrativo**: Carga de laberintos personalizados
- 🎵 **Sistema de audio**: Efectos de sonido inmersivos
- 📱 **Interfaz moderna**: Menús intuitivos y HUD informativo

## 🚀 Instalación

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

## 🎮 Cómo Jugar

### Controles
- **Flechas del teclado**: Movimiento del jugador
- **ESC**: Regresar al menú principal
- **ENTER**: Seleccionar opción / Reiniciar juego

### Objetivo
1. Navega por el laberinto usando las teclas de flecha
2. Evita ser capturado por los enemigos (⚠️)
3. Recolecta todas las estrellas (⭐) para avanzar de nivel
4. Acumula puntos y alcanza el salón de la fama

## 🏗️ Arquitectura del Proyecto

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

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
python -m pytest tests/

# Ejecutar pruebas con cobertura
python -m pytest tests/ --cov=src/
```

## 👥 Equipo de Desarrollo

- **Wendy Ulate Gutierrez**
- **Manyel Lizandro Torrez**  
- **Luis Alberto Álvarez Gómez**
- **Kendall Alvarado Artavia**

**Profesor Tutor**: Lic. Manfred Mejías Acevedo

## 📝 Licencia

Este proyecto es desarrollado con fines académicos para el curso MO-0002 Programación I de la Universidad de Costa Rica.

---

**Universidad de Costa Rica - Sede de Occidente**  
**Segundo Ciclo 2025**