import sys
import os

# Ensure project root on path and run game from src package
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    from src.juego.juego import Juego
    Juego().ejecutar()
