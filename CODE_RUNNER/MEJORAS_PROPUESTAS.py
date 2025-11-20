"""
MEJORAS PROPUESTAS Y EXTENSIONES AL JUEGO MAZE RUNNER
======================================================

Este archivo proporciona ejemplos de código para mejorar y extender
la funcionalidad del juego Maze Runner.

MEJORA 1: Sistema de Guardado de Partidas
==========================================

Implementación de guardar y cargar estado del juego:
"""

class GestorGuardado:
    """
    Gestiona guardar y cargar partidas del juego.
    """
    
    def __init__(self, ruta_guardados="guardados.json"):
        self.ruta_guardados = ruta_guardados
    
    def guardar_partida(self, juego, nombre_archivo):
        """
        Guarda el estado actual del juego.
        
        Parámetros:
        - juego: Instancia de Juego
        - nombre_archivo: Nombre del archivo de guardado
        """
        import json
        
        estado = {
            "nivel_actual": juego.nivel_actual,
            "vidas": juego.vidas,
            "puntuacion": juego.puntuacion,
            "posicion_jugador": [juego.posicion_x, juego.posicion_y],
            "enemigos": juego.enemigos,
            "estrellas": juego.estrellas,
            "potenciadores": juego.potenciadores,
            "potenciador_activo": juego.potenciador_activo,
        }
        
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                json.dump(estado, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando partida: {e}")
            return False
    
    def cargar_partida(self, juego, nombre_archivo):
        """
        Carga el estado de una partida guardada.
        """
        import json
        import os
        
        if not os.path.exists(nombre_archivo):
            return False
        
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                estado = json.load(f)
            
            juego.nivel_actual = estado["nivel_actual"]
            juego.vidas = estado["vidas"]
            juego.puntuacion = estado["puntuacion"]
            juego.posicion_x, juego.posicion_y = estado["posicion_jugador"]
            juego.enemigos = estado["enemigos"]
            juego.estrellas = estado["estrellas"]
            juego.potenciadores = estado["potenciadores"]
            juego.potenciador_activo = estado["potenciador_activo"]
            
            return True
        except Exception as e:
            print(f"Error cargando partida: {e}")
            return False


# MEJORA 2: Contador de Dificultad Progresiva
# =============================================

class NivelDificultad:
    """
    Sistema de dificultad progresiva que aumenta la velocidad
    de enemigos y reduce el número de vidas según el nivel.
    """
    
    @staticmethod
    def calcular_velocidad_enemigos(nivel_actual, velocidad_base=14):
        """
        Aumenta la velocidad de enemigos cada nivel.
        """
        incremento = nivel_actual * 2
        velocidad_nueva = min(velocidad_base + incremento, 30)  # Máximo 30
        return velocidad_nueva
    
    @staticmethod
    def calcular_vidas_iniciales(nivel_actual, vidas_base=3):
        """
        Reduce las vidas cada 3 niveles.
        """
        reduccion = (nivel_actual // 3) * 1
        vidas_nuevas = max(vidas_base - reduccion, 1)
        return vidas_nuevas


# MEJORA 3: Diferentes Tipos de Enemigos
# ========================================

class TipoEnemigo:
    """
    Diferentes comportamientos de enemigos.
    """
    
    PERSEGUIDOR = "perseguidor"      # Persigue activamente
    PATRULLERO = "patrullero"        # Patrulla un área
    ALEATORIO = "aleatorio"          # Movimiento aleatorio
    TELEPORTADOR = "teleportador"    # Se teletransporta ocasionalmente


class Enemigo:
    """
    Clase mejorada para enemigos con diferentes comportamientos.
    """
    
    def __init__(self, x, y, tipo=TipoEnemigo.PERSEGUIDOR):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.contador = 0
    
    def actualizar_posicion(self, laberinto, posicion_jugador):
        """
        Actualiza posición según el tipo de enemigo.
        """
        if self.tipo == TipoEnemigo.PERSEGUIDOR:
            return self._perseguir(laberinto, posicion_jugador)
        elif self.tipo == TipoEnemigo.PATRULLERO:
            return self._patrullar(laberinto)
        elif self.tipo == TipoEnemigo.ALEATORIO:
            return self._movimiento_aleatorio(laberinto)
        elif self.tipo == TipoEnemigo.TELEPORTADOR:
            return self._teleportador(laberinto, posicion_jugador)
    
    def _perseguir(self, laberinto, posicion_jugador):
        # Implementar BFS como en la solución original
        pass
    
    def _patrullar(self, laberinto):
        # Patrullar en un área predefinida
        pass
    
    def _movimiento_aleatorio(self, laberinto):
        # Movimiento totalmente aleatorio
        pass
    
    def _teleportador(self, laberinto, posicion_jugador):
        # Teletransportarse ocasionalmente
        import random
        
        if random.random() < 0.05:  # 5% de probabilidad
            filas, cols = len(laberinto), len(laberinto[0])
            self.x = random.randint(1, cols - 2)
            self.y = random.randint(1, filas - 2)
            if laberinto[self.y][self.x] == 1:
                self.x, self.y = posicion_jugador  # Fallback


# MEJORA 4: Sistema de Logros
# ============================

class Logro:
    """
    Representa un logro desbloqueado.
    """
    
    def __init__(self, id_logro, nombre, descripcion, icono):
        self.id = id_logro
        self.nombre = nombre
        self.descripcion = descripcion
        self.icono = icono
        self.desbloqueado = False
        self.fecha_desbloqueo = None


class GestorLogros:
    """
    Gestiona los logros del jugador.
    """
    
    LOGROS_PREDEFINIDOS = {
        "primer_nivel": Logro("primer_nivel", "Primer Paso", "Completa el primer nivel", "\u00f0"),
        "maestro_de_laberintos": Logro("maestro_de_laberintos", "Maestro de Laberintos", "Completa todos los niveles", "\u0131"),
        "coleccionista": Logro("coleccionista", "Coleccionista", "Recolecta 100 estrellas totales", "\u2605"),
        "sobreviviente": Logro("sobreviviente", "Sobreviviente", "Completa un nivel sin perder vidas", "\u2665"),
        "cazador_de_powerups": Logro("cazador_de_powerups", "Cazador de PowerUps", "Recolecta 50 potenciadores", "\u26a1"),
    }
    
    def __init__(self):
        self.logros = self.LOGROS_PREDEFINIDOS.copy()
    
    def desbloquear_logro(self, id_logro):
        """
        Desbloquea un logro.
        """
        from datetime import datetime
        
        if id_logro in self.logros:
            self.logros[id_logro].desbloqueado = True
            self.logros[id_logro].fecha_desbloqueo = datetime.now()
            print(f"¡Logro desbloqueado: {self.logros[id_logro].nombre}!")
    
    def verificar_logros(self, juego):
        """
        Verifica qué logros se deben desbloquear.
        """
        if juego.nivel_actual == 0:
            self.desbloquear_logro("primer_nivel")
        
        if juego.puntuacion >= 100:
            self.desbloquear_logro("coleccionista")


# MEJORA 5: Sistema de Sonidos
# =============================

class GestorSonidos:
    """
    Gestiona sonidos y música del juego.
    """
    
    def __init__(self):
        self.sonidos = {}
        self.musica_fondo = None
        self.volumen = 1.0
    
    def cargar_sonido(self, nombre, ruta):
        """
        Carga un efecto de sonido.
        """
        try:
            import pygame
            self.sonidos[nombre] = pygame.mixer.Sound(ruta)
            return True
        except Exception as e:
            print(f"Error cargando sonido {nombre}: {e}")
            return False
    
    def reproducir_sonido(self, nombre):
        """
        Reproduce un sonido.
        """
        if nombre in self.sonidos:
            self.sonidos[nombre].set_volume(self.volumen)
            self.sonidos[nombre].play()


# MEJORA 6: Editor de Laberintos
# ==============================

class EditorLaberintos:
    """
    Herramienta para crear y editar laberintos.
    """
    
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.laberinto = [[1 for _ in range(ancho)] for _ in range(alto)]
    
    def generar_aleatorio(self):
        """
        Genera un laberinto aleatorio usando algoritmos de generación.
        """
        import random
        
        # Algoritmo simple: llenar con 0s y crear paredes
        for y in range(1, self.alto - 1):
            for x in range(1, self.ancho - 1):
                if random.random() < 0.3:
                    self.laberinto[y][x] = 1
                else:
                    self.laberinto[y][x] = 0
    
    def exportar_a_json(self, nombre_archivo):
        """
        Exporta el laberinto a un archivo JSON.
        """
        import json
        
        nivel = {
            "nombre": "Laberinto personalizado",
            "laberinto": self.laberinto,
            "vel_enemigos": 14,
            "estrellas": 3,
            "enemigos": 2,
            "powerups": 1,
        }
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(nivel, f, indent=2, ensure_ascii=False)


# EJEMPLO DE USO DE LAS MEJORAS:

if __name__ == "__main__":
    # Ejemplo 1: Guardar partida
    # gestor = GestorGuardado()
    # gestor.guardar_partida(juego, "mi_partida.json")
    
    # Ejemplo 2: Dificultad progresiva
    # velocidad = NivelDificultad.calcular_velocidad_enemigos(5)
    # vidas = NivelDificultad.calcular_vidas_iniciales(3)
    
    # Ejemplo 3: Gestor de logros
    # gestor_logros = GestorLogros()
    # gestor_logros.verificar_logros(juego)
    
    # Ejemplo 4: Editor de laberintos
    # editor = EditorLaberintos(15, 11)
    # editor.generar_aleatorio()
    # editor.exportar_a_json("mi_laberinto.json")
    
    print("Ejemplos de mejoras cargados exitosamente.")
"""
