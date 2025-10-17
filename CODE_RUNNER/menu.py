class Menu:
    """
    Clase base para los menús del juego.
    """
    def __init__(self, opciones):
        if not (isinstance(opciones, list) and all(isinstance(op, str) for op in opciones)):
            raise ValueError("Las opciones deben ser una lista de strings.")
        self._opciones = opciones
        self._seleccion = None

    @property
    def opciones(self):
        return self._opciones

    @property
    def seleccion(self):
        return self._seleccion

    def mostrar_menu(self):
        """
        Muestra las opciones del menú.
        """
        for idx, opcion in enumerate(self._opciones, 1):
            print(f"{idx}. {opcion}")

    def ejecutar_seleccion(self, opcion_seleccionada):
        """
        Define la acción a ejecutar según la opción seleccionada.
        Este método debe ser sobreescrito en subclases.
        """
        if not (isinstance(opcion_seleccionada, int) and 1 <= opcion_seleccionada <= len(self._opciones)):
            raise ValueError("La opción seleccionada no es válida.")
        self._seleccion = opcion_seleccionada
        # Implementar en subclases

class MenuDeInicio(Menu):
    def __init__(self):
        opciones = ["Comenzar juego", "Salir"]
        super().__init__(opciones)

    def ejecutar_seleccion(self, opcion_seleccionada):
        super().ejecutar_seleccion(opcion_seleccionada)
        if opcion_seleccionada == 1:
            print("Iniciando juego...")
            # Lógica para iniciar el juego
        elif opcion_seleccionada == 2:
            print("Saliendo del juego...")
            # Lógica para salir

class MenuAdministrador(Menu):
    def __init__(self):
        opciones = ["Eliminar lista", "Nueva lista", "Cargar laberintos"]
        super().__init__(opciones)

    def ejecutar_seleccion(self, opcion_seleccionada):
        super().ejecutar_seleccion(opcion_seleccionada)
        if opcion_seleccionada == 1:
            print("Eliminando lista...")
            # Lógica para eliminar lista
        elif opcion_seleccionada == 2:
            print("Creando nueva lista...")
            # Lógica para nueva lista
        elif opcion_seleccionada == 3:
            print("Cargando laberintos...")
            # Lógica para cargar laberintos


