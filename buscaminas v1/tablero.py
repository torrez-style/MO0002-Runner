# tablero.py
import random
from celdas import Celdas

class Tablero:
    """Define la clase general del tablero para Buscaminas.
    Inicializa una matriz de objetos Celda, coloca minas y calcula vecinos."""

    def __init__(self, tamanno, num_minas):
        self.tamanno = tamanno
        self.num_minas = num_minas
        # Crea una matriz (lista de listas) de objetos Celda.
        self._matriz_tablero = [[Celdas() for _ in range(tamanno)] for _ in range(tamanno)]
        self._celdas_reveladas = 0
        self._juego_terminado = False

        self._colocar_minas_aleatorias()
        self._calcular_contadores_vecinos()

    def _colocar_minas_aleatorias(self):
        """Distribuye las minas al azar en el tablero."""
        minas_colocadas = 0
        while minas_colocadas < self.num_minas:
            r = random.randint(0, self.tamanno - 1)
            c = random.randint(0, self.tamanno - 1)

            celda = self._matriz_tablero[r][c]
            if not celda.es_mina():
                celda.colocar_mina()
                minas_colocadas += 1

    def _obtener_vecinos(self, r, c):
        """Generador que retorna las coordenadas (fila, columna) de las celdas vecinas."""
        # Se revisan las 8 direcciones (incluyendo diagonales)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # No revisar la celda actual

                nr, nc = r + dr, c + dc
                # Verificar que la coordenada esté dentro del tablero
                if 0 <= nr < self.tamanno and 0 <= nc < self.tamanno:
                    yield nr, nc

    def _calcular_contadores_vecinos(self):
        """Recorre el tablero y establece el contador de minas vecinas para cada celda no minada."""
        for r in range(self.tamanno):
            for c in range(self.tamanno):
                celda = self._matriz_tablero[r][c]
                if not celda.es_mina():
                    minas_cercanas = 0
                    for nr, nc in self._obtener_vecinos(r, c):
                        if self._matriz_tablero[nr][nc].es_mina():
                            minas_cercanas += 1
                    
                    # Usamos el método de la celda para establecer el contador
                    for _ in range(minas_cercanas):
                        celda.incrementar_contador()

    def revelar_celda(self, r, c):
        """Revela una celda y ejecuta la lógica del juego."""
        if not (0 <= r < self.tamanno and 0 <= c < self.tamanno) or self._juego_terminado:
            return False # Coordenadas inválidas o juego terminado

        celda = self._matriz_tablero[r][c]
        if celda.esta_revelada():
            return False # Ya estaba revelada

        celda.revelar()
        self._celdas_reveladas += 1

        # 1. Si es una mina, el juego termina.
        if celda.es_mina():
            self._juego_terminado = True
            print("¡BOOM!  Has encontrado una mina. ¡Juego Terminado!")
            self._revelar_todas_las_minas() # Mostrar todas las minas al perder
            return True

        # 2. Si no tiene minas vecinas, revelar recursivamente a sus vecinos.
        if celda._mina_vecina_contador == 0:
            for nr, nc in self._obtener_vecinos(r, c):
                self.revelar_celda(nr, nc) # Llamada recursiva

        # 3. Comprobar si ganó
        if self._celdas_reveladas == (self.tamanno * self.tamanno) - self.num_minas:
            self._juego_terminado = True
            print("¡FELICIDADES!  Has revelado todas las celdas seguras. ¡Ganaste!")

        return True

    def imprimir_tablero(self):
        """Muestra el tablero en la terminal de forma legible."""
        print(f"\n--- Buscaminas {self.tamanno}x{self.tamanno} (Minas: {self.num_minas}) ---")
        
        # 1. Imprimir la cabecera con los números de columna
        #    '  ' es para alinear con los números de fila
        header = "  " + " ".join([str(i % 10) for i in range(self.tamanno)]) # Usar módulo 10 para mejor visualización en tamaños grandes
        print(header)
        
        # 2. Imprimir cada fila
        for r in range(self.tamanno):
            # Imprime el número de fila (r) seguido de los valores de la fila
            fila_str = f"{r % 10} " + " ".join([self._matriz_tablero[r][c].obtener_valor_a_mostrar()
                                            for c in range(self.tamanno)])
            print(fila_str)
        print("---------------------------------")

    def esta_terminado(self):
        """Retorna el estado del juego."""
        return self._juego_terminado

    def _revelar_todas_las_minas(self):
        """Revela todas las celdas para mostrar el resultado final."""
        for r in range(self.tamanno):
            for c in range(self.tamanno):
                if self._matriz_tablero[r][c].es_mina():
                    self._matriz_tablero[r][c].revelar()