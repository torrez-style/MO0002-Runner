
# jugar.py
from tablero import Tablero

class Jugar:
    """Clase principal que coordina la creación, visualización y jugabilidad del Tablero."""

    def __init__(self, tamanno):
        # Determinar un número de minas basado en el tamaño, aproximadamente el 15-20% del área.
        num_minas = max(1, int((tamanno * tamanno) * 0.17)) 
        
        # Crear la instancia del tablero
        self._tablero = Tablero(tamanno, num_minas)
        self._tamanno = tamanno

    def _capturar_movimiento(self):
        """Solicita y valida las coordenadas de la celda a revelar."""
        while True:
            try:
                # Pedir al usuario las coordenadas
                entrada = input(f"Ingrese Fila y Columna separadas por un espacio (ej: 0 4): ").strip()
                if not entrada:
                    continue
                
                # Intentar parsear a números enteros
                partes = entrada.split()
                if len(partes) != 2:
                    print("Formato incorrecto. Debe ser Fila <espacio> Columna.")
                    continue

                r, c = int(partes[0]), int(partes[1])
                
                # Validar que estén dentro del rango
                if 0 <= r < self._tamanno and 0 <= c < self._tamanno:
                    return r, c
                else:
                    print(f"Coordenadas fuera del tablero. Use números entre 0 y {self._tamanno - 1}.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese solo números enteros.")
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")


    def vamos_a_jugar(self):
        """Contiene el bucle principal del juego."""
        print("\n¡Bienvenido al Buscaminas de la Terminal!")
        print("El objetivo es revelar todas las celdas seguras sin explotar una mina (*).")
        
        while not self._tablero.esta_terminado():
            # 1. Mostrar el estado actual del tablero
            self._tablero.imprimir_tablero()
            
            # 2. Solicitar el siguiente movimiento
            r, c = self._capturar_movimiento()
            
            # 3. Revelar la celda seleccionada
            
            "Se implemneto resultado="
            resultado  = self._tablero.revelar_celda(r, c)
            if not resultado:
                print("Esta posición ya fue revelada.\nIntenta otra coordenada.")
            
        # Al salir del bucle (juego terminado por victoria o derrota)
        self._tablero.imprimir_tablero() # Mostrar el tablero final
        print("\nFin del juego. ¡Gracias por jugar!")
    
