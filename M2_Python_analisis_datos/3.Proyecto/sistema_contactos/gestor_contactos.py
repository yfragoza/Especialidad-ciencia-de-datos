from contacto import Contacto


class GestorContactos:
    def __init__(self):
        self.contactos = []

    def agregar_contacto(self, nombre, telefono, correo, direccion):
        if self.buscar_por_telefono(telefono) is not None:
            return False
        nuevo = Contacto(nombre, telefono, correo, direccion)
        self.contactos.append(nuevo)
        return True

    def listar_contactos(self):
        return self.contactos

    def buscar_por_nombre(self, nombre):
        resultados = []
        for contacto in self.contactos:
            if nombre.lower() in contacto.get_nombre().lower():
                resultados.append(contacto)
        return resultados

    def buscar_por_telefono(self, telefono):
        for contacto in self.contactos:
            if contacto.get_telefono() == telefono:
                return contacto
        return None

    def editar_contacto(self, telefono, nuevo_nombre=None, nuevo_telefono=None,
                        nuevo_correo=None, nueva_direccion=None):
        contacto = self.buscar_por_telefono(telefono)
        if contacto is None:
            return False

        if nuevo_telefono and nuevo_telefono != telefono:
            if self.buscar_por_telefono(nuevo_telefono) is not None:
                return False

        if nuevo_nombre:
            contacto.set_nombre(nuevo_nombre)
        if nuevo_telefono:
            contacto.set_telefono(nuevo_telefono)
        if nuevo_correo:
            contacto.set_correo(nuevo_correo)
        if nueva_direccion:
            contacto.set_direccion(nueva_direccion)

        return True

    def eliminar_contacto(self, telefono):
        contacto = self.buscar_por_telefono(telefono)
        if contacto is None:
            return False
        self.contactos.remove(contacto)
        return True