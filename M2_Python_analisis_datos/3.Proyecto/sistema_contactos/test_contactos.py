import unittest
from gestor_contactos import GestorContactos


class TestGestorContactos(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorContactos()
        self.gestor.agregar_contacto(
            "Ana Pérez", "123456789", "ana@email.com", "Santiago"
        )

    def test_agregar_contacto(self):
        resultado = self.gestor.agregar_contacto(
            "Luis Gómez", "987654321", "luis@email.com", "Providencia"
        )
        self.assertTrue(resultado)
        self.assertEqual(len(self.gestor.listar_contactos()), 2)

    def test_no_agregar_telefono_duplicado(self):
        resultado = self.gestor.agregar_contacto(
            "Otra Ana", "123456789", "otra@email.com", "Maipú"
        )
        self.assertFalse(resultado)

    def test_buscar_por_nombre(self):
        resultados = self.gestor.buscar_por_nombre("Ana")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].get_nombre(), "Ana Pérez")

    def test_buscar_por_telefono(self):
        contacto = self.gestor.buscar_por_telefono("123456789")
        self.assertIsNotNone(contacto)
        self.assertEqual(contacto.get_correo(), "ana@email.com")

    def test_editar_contacto(self):
        resultado = self.gestor.editar_contacto(
            "123456789", nuevo_nombre="Ana María"
        )
        self.assertTrue(resultado)
        contacto = self.gestor.buscar_por_telefono("123456789")
        self.assertEqual(contacto.get_nombre(), "Ana María")

    def test_eliminar_contacto(self):
        resultado = self.gestor.eliminar_contacto("123456789")
        self.assertTrue(resultado)
        self.assertEqual(len(self.gestor.listar_contactos()), 0)


if __name__ == "__main__":
    unittest.main()