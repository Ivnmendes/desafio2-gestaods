
from unittest import TestCase
from src.core.value_objects import Nome

class TestValueObjects(TestCase):

    def test_criar_nome_valido(self):

        nome = Nome("John Doe")

        self.assertEqual("John Doe", nome.valor)

    def test_criar_nome_vazio(self):
        
        with self.assertRaises(ValueError):
            Nome("")