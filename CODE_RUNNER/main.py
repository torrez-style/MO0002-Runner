import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.juego.juego import Juego

if __name__ == "__main__":
    Juego().ejecutar()
