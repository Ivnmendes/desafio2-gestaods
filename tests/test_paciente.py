
from unittest import TestCase
from src.paciente import Paciente

class TestPaciente(TestCase):

    def test_criar_paciente(self):

        paciente = Paciente(
            nome = "Foreman"
        )

        self.assertIsInstance(paciente, Paciente)

    def test_nao_criar_paciente_sem_nome(self):

        with self.assertRaises(ValueError):
            paciente = Paciente(
                nome = ""
            )