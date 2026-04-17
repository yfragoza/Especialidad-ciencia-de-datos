from gestor_contactos import GestorContactos


def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN DE CONTACTOS ===")
    print("1. Agregar contacto")
    print("2. Listar contactos")
    print("3. Buscar contacto por nombre")
    print("4. Buscar contacto por teléfono")
    print("5. Editar contacto")
    print("6. Eliminar contacto")
    print("7. Salir")


def pedir_datos_contacto():
    nombre = input("Nombre: ").strip()
    telefono = input("Teléfono: ").strip()
    correo = input("Correo: ").strip()
    direccion = input("Dirección: ").strip()
    return nombre, telefono, correo, direccion


def main():
    gestor = GestorContactos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre, telefono, correo, direccion = pedir_datos_contacto()
            if gestor.agregar_contacto(nombre, telefono, correo, direccion):
                print("Contacto agregado correctamente.")
            else:
                print("No se pudo agregar. Ya existe un contacto con ese teléfono.")

        elif opcion == "2":
            contactos = gestor.listar_contactos()
            if not contactos:
                print("No hay contactos registrados.")
            else:
                print("\n--- LISTA DE CONTACTOS ---")
                for contacto in contactos:
                    print(contacto)

        elif opcion == "3":
            nombre = input("Ingrese el nombre a buscar: ").strip()
            resultados = gestor.buscar_por_nombre(nombre)
            if resultados:
                print("\nResultados encontrados:")
                for contacto in resultados:
                    print(contacto)
            else:
                print("No se encontraron contactos con ese nombre.")

        elif opcion == "4":
            telefono = input("Ingrese el teléfono a buscar: ").strip()
            contacto = gestor.buscar_por_telefono(telefono)
            if contacto:
                print("\nContacto encontrado:")
                print(contacto)
            else:
                print("No se encontró un contacto con ese teléfono.")

        elif opcion == "5":
            telefono = input("Ingrese el teléfono del contacto a editar: ").strip()
            print("Deje en blanco los campos que no desea modificar.")
            nuevo_nombre = input("Nuevo nombre: ").strip()
            nuevo_telefono = input("Nuevo teléfono: ").strip()
            nuevo_correo = input("Nuevo correo: ").strip()
            nueva_direccion = input("Nueva dirección: ").strip()

            exito = gestor.editar_contacto(
                telefono,
                nuevo_nombre if nuevo_nombre else None,
                nuevo_telefono if nuevo_telefono else None,
                nuevo_correo if nuevo_correo else None,
                nueva_direccion if nueva_direccion else None
            )

            if exito:
                print("Contacto editado correctamente.")
            else:
                print("No se pudo editar el contacto.")

        elif opcion == "6":
            telefono = input("Ingrese el teléfono del contacto a eliminar: ").strip()
            if gestor.eliminar_contacto(telefono):
                print("Contacto eliminado correctamente.")
            else:
                print("No se encontró un contacto con ese teléfono.")

        elif opcion == "7":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()