from datetime import date, datetime, time
from unittest import TestCase

from agenda.agenda import Agenda
from core.exceptions import HorarioIndisponivelException
from core.utils import Dias
from medico.medico import Medico
from paciente.paciente import Paciente


class TestAgenda(TestCase):

    medico_1 = Medico(
        nome="Dr House",
        hora_inicio=time(hour=8, minute=30),
        hora_fim=time(hour=14, minute=30),
        lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
    )
    medico_2 = Medico(
        nome="Treze",
        hora_inicio=time(hour=10, minute=30),
        hora_fim=time(hour=16, minute=30),
        lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.SEXTA],
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
        self.assertEqual(self.medico_1, agenda.medico)

    def test_nao_criar_agenda_com_datas_invalidas(self):

        with self.assertRaises(ValueError):
            Agenda(
                self.medico_1,
                data_inicio=date(year=2026, month=4, day=1),
                data_fim=date(year=2026, month=3, day=30),
            )

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

    def test_verificar_se_paciente_tem_agendamento(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        agenda.agendar_horario(
            self.paciente_1, datetime(year=2026, month=4, day=2, hour=9, minute=30)
        )

        self.assertTrue(self.paciente_1 in agenda)
        self.assertFalse(self.paciente_2 in agenda)

    def test_contar_agendamentos(self):

        agenda = Agenda(
            self.medico_1,
            data_inicio=date(year=2026, month=4, day=1),
            data_fim=date(year=2026, month=4, day=30),
        )

        agenda.agendar_horario(
            self.paciente_1, datetime(year=2026, month=4, day=2, hour=9, minute=30)
        )
        agenda.agendar_horario(
            self.paciente_2, datetime(year=2026, month=4, day=2, hour=10, minute=30)
        )

        self.assertEqual(2, len(agenda))