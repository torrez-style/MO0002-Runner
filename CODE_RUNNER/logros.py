import json
import os
from datetime import datetime

class Logro:
    def __init__(self, id_logro, nombre, descripcion, icono):
        self.id = id_logro
        self.nombre = nombre
        self.descripcion = descripcion
        self.icono = icono
        self.desbloqueado = False
        self.fecha_desbloqueo = None

class GestorLogros:
    LOGROS_PREDEFINIDOS = {
        "primer_nivel": Logro("primer_nivel", "Primer Paso", "Completa el primer nivel", "★"),
        "maestro_de_laberintos": Logro("maestro_de_laberintos", "Maestro de Laberintos", "Completa todos los niveles", "🏆"),
        "coleccionista": Logro("coleccionista", "Coleccionista", "Recolecta 100 estrellas", "⭐"),
        "sobreviviente": Logro("sobreviviente", "Sobreviviente", "Completa un nivel sin perder vidas", "❤️"),
        "cazador_de_powerups": Logro("cazador_de_powerups", "Cazador de PowerUps", "Recolecta 50 potenciadores", "⚡"),
    }

    def __init__(self, usuario=None):
        self.usuario = usuario if usuario else "INVITADO"
        self.logros = {k: Logro(v.id, v.nombre, v.descripcion, v.icono) for k, v in self.LOGROS_PREDEFINIDOS.items()}
        self._cargar_desbloqueados()

    def desbloquear_logro(self, id_logro):
        if id_logro in self.logros:
            self.logros[id_logro].desbloqueado = True
            self.logros[id_logro].fecha_desbloqueo = datetime.now().isoformat()
            self._guardar_desbloqueados()

    def verificar_y_desbloquear(self, juego):
        if juego.nivel_actual == 0:
            self.desbloquear_logro("primer_nivel")
        if juego.puntuacion >= 100:
            self.desbloquear_logro("coleccionista")
        # más condiciones específicas aquí

    def listar_logros_desbloqueados(self):
        return [v.nombre for v in self.logros.values() if v.desbloqueado]

    def _guardar_desbloqueados(self):
        ruta = f"CODE_RUNNER/logros_{self.usuario}.json"
        guardar = {}
        for k, v in self.logros.items():
            if v.desbloqueado:
                guardar[k] = {'nombre': v.nombre, 'fecha': v.fecha_desbloqueo}
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(guardar, archivo, indent=2, ensure_ascii=False)

    def _cargar_desbloqueados(self):
        ruta = f"CODE_RUNNER/logros_{self.usuario}.json"
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as archivo:
                data = json.load(archivo)
            for k in data:
                if k in self.logros:
                    self.logros[k].desbloqueado = True
                    self.logros[k].fecha_desbloqueo = data[k]['fecha']
