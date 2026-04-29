from unittest import TestCase

from paciente.paciente import Paciente


class TestPaciente(TestCase):

    def test_criar_paciente(self):

        paciente = Paciente(nome="Foreman")

        self.assertIsInstance(paciente, Paciente)
        self.assertEqual("Foreman", paciente.nome)

    def test_nao_criar_paciente_sem_nome(self):

        with self.assertRaises(ValueError):
            Paciente(nome="")
