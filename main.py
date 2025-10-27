#!/usr/bin/env python3
"""
Maze Runner - Punto de entrada principal
Juego de laberinto desarrollado en Python con Pygame

MO0002 - Programación I - Universidad de Costa Rica
Autores: Wendy Ulate Gutierrez, Manyel Lizandro Torrez, 
         Luis Alberto Álvarez Gómez, Kendall Alvarado Artavia
Profesor: Lic. Manfred Mejías Acevedo
Segundo Ciclo 2025
"""

import sys
import os
import traceback
from pathlib import Path

# Añadir el directorio raíz al path para imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # Importar dependencias principales
    import pygame
    
    # Verificar versión de Python
    if sys.version_info < (3, 8):
        raise RuntimeError("Maze Runner requiere Python 3.8 o superior")
    
    # Importar módulos del juego
    from src.core.game_engine import GameEngine
    from config.settings import settings
    
except ImportError as e:
    print(f"ERROR de importación: {e}")
    print("\nPosibles soluciones:")
    print("1. Instalar dependencias: pip install -r requirements.txt")
    print("2. Verificar que está en el directorio correcto del proyecto")
    print("3. Verificar instalación de Python")
    sys.exit(1)
except Exception as e:
    print(f"ERROR inesperado durante la importación: {e}")
    traceback.print_exc()
    sys.exit(1)


def check_system_requirements() -> bool:
    """
    Verifica los requisitos del sistema antes de iniciar el juego
    
    Returns:
        True si todos los requisitos se cumplen, False si no
    """
    try:
        # Verificar pygame
        pygame_version = pygame.version.ver
        print(f"Pygame versión: {pygame_version}")
        
        # Verificar inicialización de video
        pygame.init()
        if not pygame.get_init():
            print("No se pudo inicializar Pygame")
            return False
        
        # Verificar capacidades de video
        try:
            _ = pygame.display.set_mode((1, 1))
            pygame.display.quit()
            print("Sistema de video disponible")
        except pygame.error:
            print("Sistema de video no disponible")
            return False
        
        # Verificar capacidades de audio
        try:
            pygame.mixer.init()
            if pygame.mixer.get_init():
                print("Sistema de audio disponible")
                pygame.mixer.quit()
            else:
                print("Sistema de audio no disponible (el juego continuará sin sonido)")
        except pygame.error:
            print("Sistema de audio no disponible (el juego continuará sin sonido)")
        
        return True
        
    except Exception as e:
        print(f"Error verificando requisitos del sistema: {e}")
        return False


def create_required_directories() -> None:
    """
    Crea los directorios necesarios para el juego si no existen
    """
    required_dirs = [
        "assets",
        "assets/sounds",
        "assets/config",
        "assets/data",
        "logs"
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"Directorio creado: {dir_path}")
            except OSError as e:
                print(f"No se pudo crear directorio {dir_path}: {e}")


def setup_logging() -> None:
    """
    Configura el sistema de logging del juego
    """
    import logging
    from datetime import datetime
    
    # Crear directorio de logs si no existe
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configurar logging
    log_filename = logs_dir / f"maze_runner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger('MazeRunner')
    logger.info("Sistema de logging inicializado")
    logger.info(f"Archivo de log: {log_filename}")


def display_welcome_message() -> None:
    """
    Muestra el mensaje de bienvenida del juego
    """
    welcome_art = """
╔══════════════════════════════════════════════╗
║                MAZE RUNNER                   ║
╠══════════════════════════════════════════════╣
║  MO0002 - Programación I                     ║
║  Universidad de Costa Rica - Sede de Occidente║
║  Segundo Ciclo 2025                          ║
╠══════════════════════════════════════════════╣
║  Autores:                                    ║
║  • Wendy Ulate Gutierrez                     ║
║  • Manyel Lizandro Torrez                    ║
║  • Luis Alberto Álvarez Gómez                ║
║  • Kendall Alvarado Artavia                  ║
╠══════════════════════════════════════════════╣
║  Profesor: Lic. Manfred Mejías Acevedo       ║
╚══════════════════════════════════════════════╝
    """
    
    print(welcome_art)
    print(f"Version del juego: 2.0.0")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Pygame: {pygame.version.ver}")
    print(f"Resolucion: {settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}")
    print(f"FPS objetivo: {settings.FPS}")
    print()


def handle_startup_error(error: Exception) -> None:
    """
    Maneja errores durante el inicio del juego
    
    Args:
        error: Excepción que ocurrió
    """
    print(f"\nERROR DURANTE EL INICIO: {error}")
    print("\nInformación de debugging:")
    print("-" * 50)
    traceback.print_exc()
    print("-" * 50)
    
    print("\nPosibles soluciones:")
    print("1. Verificar instalación de dependencias: pip install -r requirements.txt")
    print("2. Verificar permisos de escritura en el directorio")
    print("3. Verificar drivers de video/audio del sistema")
    print("4. Ejecutar desde el directorio raíz del proyecto")
    print("5. Verificar compatibilidad del sistema operativo")
    
    print("\nPara soporte, contactar al equipo de desarrollo")


def main() -> int:
    """
    Función principal del programa
    
    Returns:
        Código de salida (0 = éxito, 1 = error)
    """
    try:
        # Mostrar mensaje de bienvenida
        display_welcome_message()
        
        # Configurar logging
        setup_logging()
        
        # Verificar requisitos del sistema
        print("Verificando requisitos del sistema...")
        if not check_system_requirements():
            print("Los requisitos del sistema no se cumplen")
            return 1
        
        # Crear directorios necesarios
        print("Creando directorios necesarios...")
        create_required_directories()
        
        # Inicializar y ejecutar el motor del juego
        print("Inicializando motor del juego...")
        game_engine = GameEngine()
        
        print("Iniciando Maze Runner...")
        print("\n" + "="*50)
        print("Controles:")
        print("   Flechas: Mover jugador")
        print("   ESC    : Menú principal")
        print("   ENTER  : Seleccionar/Reiniciar")
        print("="*50 + "\n")
        
        # Ejecutar juego
        game_engine.run()
        
        print("Juego terminado exitosamente")
        return 0
        
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido por el usuario")
        return 0
        
    except Exception as e:
        handle_startup_error(e)
        return 1
        
    finally:
        # Cleanup final
        try:
            pygame.quit()
        except:
            pass
        
        print("\nGracias por jugar Maze Runner!")
        print("Universidad de Costa Rica - Sede de Occidente")


if __name__ == "__main__":
    # Verificar que se está ejecutando como script principal
    exit_code = main()
    sys.exit(exit_code)