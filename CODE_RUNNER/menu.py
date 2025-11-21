import json
from salon_de_la_fama import SalonDeLaFama
from lista_usuarios import ListaUsuarios


class MenuPrincipal:
    def __init__(self, vista, administrador_eventos):
                        self.vista = vista
        self.administrador_eventos = administrador_eventos
        self.salon = SalonDeLaFama()
        self.lista_usuarios = ListaUsuarios()
        self.contrasena_admin = "admin123"
        self.listar_usuarios = False
        self.mostrar_salon = False

    def mostrar_menu_principal(self):
        print("\n=== MAZE RUNNER ===")
        print("1. Jugar")
        print("2. Salón de la Fama")
        print("3. Gestionar Usuarios (Admin)")
        print("4. Salir")
        opcion = input("Selecciona una opción: ").strip()
        return opcion

    def gestionar_usuarios(self):
        contrasena = input("Ingresa la contraseña de administrador: ")
        if contrasena != self.contrasena_admin:
            print("Contraseña incorrecta.")
            return

        while True:
            print("\n=== GESTIÓN DE USUARIOS ===")
            print("1. Crear usuario")
            print("2. Eliminar usuario")
            print("3. Listar usuarios")
            print("4. Volver")
            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                nombre = input("Ingresa el nombre de usuario: ").strip().upper()
                if self.lista_usuarios.crear_usuario(nombre):
                    print(f"Usuario '{nombre}' creado exitosamente.")
                else:
                    print(f"El usuario '{nombre}' ya existe.")

            elif opcion == "2":
                nombre = (
                    input("Ingresa el nombre de usuario a eliminar: ").strip().upper()
                )
                if self.lista_usuarios.eliminar_usuario(nombre):
                    print(f"Usuario '{nombre}' eliminado exitosamente.")
                    self.salon.eliminar_puntuaciones_usuario(nombre)
                else:
                    print(f"El usuario '{nombre}' no existe.")

            elif opcion == "3":
                self.lista_usuarios.listar_todos()

            elif opcion == "4":
                break

            else:
                print("Opción inválida.")

    def mostrar_salones(self):
        print("\n=== SALÓN DE LA FAMA ===")
        print(self.salon.obtener_ranking_global())
