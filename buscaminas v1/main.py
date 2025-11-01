"""Inicia el juego y solicita el tamaño."""
from jugar import Jugar


def capturar_tamanno():
    """Solicita y valida el tamaño del tablero (entre 5 y 15)."""
    while True:
        try:
            valor = int(input("Por favor, digita el tamaño del tablero (entre 5 y 15): "))
            
            if 5 <= valor <= 15:
                return valor
            else:
                print("Valor fuera del rango. Digite un número entre 5 y 15.")
        except ValueError:
            print("Entrada inválida. Por favor, digita un número entero.")

def main():
    # Solicitar el tamaño del tablero
    mi_tamanno = capturar_tamanno()
    
    # Crear el juego (que a su vez crea el Tablero)
    mi_juego = Jugar(mi_tamanno)
    
    # Ejecutamos el juego (bucle principal)
    mi_juego.vamos_a_jugar()

if __name__ == '__main__':
    main()