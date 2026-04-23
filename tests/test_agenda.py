
from unittest import TestCase
from datetime import time
from src.agenda import Agenda, DIA, DURACAO_CONSULTA
from src.medico import Medico
from src.paciente import Paciente
from src.utils import gerar_lista_horarios

class TestAgenda(TestCase):

    medico_1 = Medico(
        nome = "Dr House",
        hora_inicio = time(
            hour = 8,
            minute = 30
        ),
        hora_fim = time(
            hour = 14,
            minute = 30
        )
    )
    medico_2 = Medico(
        nome = "Treze",
        hora_inicio = time(
            hour = 10,
            minute = 30
        ),
        hora_fim = time(
            hour = 16,
            minute = 30
        )
    )
    
    paciente_1 = Paciente(
        nome = "Foreman"
    )
    paciente_2 = Paciente(
        nome = "Wilson"
    )

    def test_criar_agenda(self):

        agenda = Agenda(
            DIA.SEGUNDA,
            self.medico_1
        )

        chaves_horarios = gerar_lista_horarios(
            hora_inicio = self.medico_1.hora_inicio,
            hora_fim = self.medico_1.hora_fim,
            intervalo_minutos = DURACAO_CONSULTA
        )

        self.assertEqual(chaves_horarios, list(agenda.agendamentos.keys()))