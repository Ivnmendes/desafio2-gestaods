from datetime import date, datetime, time
from unittest import TestCase

from src.agenda.agenda import Agenda
from src.core.exceptions import HorarioIndisponivelException
from src.core.utils import DIAS
from src.medico.medico import Medico
from src.paciente.paciente import Paciente


class TestAgenda(TestCase):

    medico_1 = Medico(
        nome="Dr House",
        hora_inicio=time(hour=8, minute=30),
        hora_fim=time(hour=14, minute=30),
        lista_dias=[DIAS.SEGUNDA, DIAS.TERCA, DIAS.QUARTA, DIAS.QUINTA, DIAS.SEXTA],
    )
    medico_2 = Medico(
        nome="Treze",
        hora_inicio=time(hour=10, minute=30),
        hora_fim=time(hour=16, minute=30),
        lista_dias=[DIAS.SEGUNDA, DIAS.TERCA, DIAS.SEXTA],
    )

    paciente_1 = Paciente(nome="Foreman")
    paciente_2 = Paciente(nome="Wilson")

    def test_criar_agenda(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=2),
        )

        lista_datetimes = [
            datetime(year=2026, month=4, day=1, hour=8, minute=30),
            datetime(year=2026, month=4, day=1, hour=9, minute=0),
            datetime(year=2026, month=4, day=1, hour=9, minute=30),
            datetime(year=2026, month=4, day=1, hour=10, minute=0),
            datetime(year=2026, month=4, day=1, hour=10, minute=30),
            datetime(year=2026, month=4, day=1, hour=11, minute=0),
            datetime(year=2026, month=4, day=1, hour=11, minute=30),
            datetime(year=2026, month=4, day=1, hour=12, minute=0),
            datetime(year=2026, month=4, day=1, hour=12, minute=30),
            datetime(year=2026, month=4, day=1, hour=13, minute=0),
            datetime(year=2026, month=4, day=1, hour=13, minute=30),
            datetime(year=2026, month=4, day=1, hour=14, minute=0),
            datetime(year=2026, month=4, day=1, hour=14, minute=30),
            datetime(year=2026, month=4, day=2, hour=8, minute=30),
            datetime(year=2026, month=4, day=2, hour=9, minute=0),
            datetime(year=2026, month=4, day=2, hour=9, minute=30),
            datetime(year=2026, month=4, day=2, hour=10, minute=0),
            datetime(year=2026, month=4, day=2, hour=10, minute=30),
            datetime(year=2026, month=4, day=2, hour=11, minute=0),
            datetime(year=2026, month=4, day=2, hour=11, minute=30),
            datetime(year=2026, month=4, day=2, hour=12, minute=0),
            datetime(year=2026, month=4, day=2, hour=12, minute=30),
            datetime(year=2026, month=4, day=2, hour=13, minute=0),
            datetime(year=2026, month=4, day=2, hour=13, minute=30),
            datetime(year=2026, month=4, day=2, hour=14, minute=0),
            datetime(year=2026, month=4, day=2, hour=14, minute=30),
        ]

        self.assertEqual(lista_datetimes, list(agenda.agendamentos.keys()))

    def test_agendar_horario(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        agenda.agendar_horario(
            self.paciente_1, datetime(year=2026, month=4, day=2, hour=9, minute=30)
        )

        self.assertTrue(self.paciente_1 in agenda)

    def test_agendar_horario_invalido(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        with self.assertRaises(HorarioIndisponivelException):
            agenda.agendar_horario(
                self.paciente_1, datetime(year=2026, month=4, day=2, hour=9, minute=32)
            )

    def test_nao_agendar_sobreposicao_horario(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        agenda.agendar_horario(
            self.paciente_1, datetime(year=2026, month=4, day=2, hour=9, minute=30)
        )

        with self.assertRaises(HorarioIndisponivelException):
            agenda.agendar_horario(
                self.paciente_2, datetime(year=2026, month=4, day=2, hour=9, minute=30)
            )

    def test_verificar_horario_disponivel(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        agenda.agendar_horario(
            self.paciente_1, datetime(year=2026, month=4, day=2, hour=9, minute=30)
        )

        self.assertFalse(
            agenda.verificar_horario_disponivel(
                datetime(year=2026, month=4, day=2, hour=9, minute=30)
            )
        )
        self.assertTrue(
            agenda.verificar_horario_disponivel(
                datetime(year=2026, month=4, day=2, hour=10, minute=30)
            )
        )

    def test_desmarcar_horario(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        agenda.agendar_horario(
            self.paciente_1, datetime(year=2026, month=4, day=2, hour=9, minute=30)
        )

        agenda.desmarcar_horario(datetime(year=2026, month=4, day=2, hour=9, minute=30))

        self.assertTrue(
            agenda.verificar_horario_disponivel(
                datetime(year=2026, month=4, day=2, hour=9, minute=30)
            )
        )

    def test_desmarcar_horario_inexistente(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        with self.assertRaises(HorarioIndisponivelException):
            agenda.desmarcar_horario(
                datetime(year=2026, month=4, day=2, hour=15, minute=30)
            )
