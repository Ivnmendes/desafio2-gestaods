
from unittest import TestCase
from src.medico.value_objects import (
    IntervaloHorario,
    DiasAtendimento
)
from datetime import time
from src.core.utils import DIAS

class TestIntervaloHorario(TestCase):

    def test_intervalo_horario_valido(self):
        intervalo = IntervaloHorario(hora_inicio=time(8, 0), hora_fim=time(17, 0))
        self.assertEqual(intervalo.hora_inicio, time(8, 0))
        self.assertEqual(intervalo.hora_fim, time(17, 0))

    def test_intervalo_horario_invalido(self):
        with self.assertRaises(ValueError):
            IntervaloHorario(hora_inicio=time(17, 0), hora_fim=time(8, 0))

class TestDiasAtendimento(TestCase):

    def test_dias_atendimento_validos(self):
        dias = DiasAtendimento(lista_dias=[DIAS.SEGUNDA, DIAS.QUARTA, DIAS.SEXTA])
        self.assertEqual(dias.valor, [DIAS.SEGUNDA, DIAS.QUARTA, DIAS.SEXTA])

    def test_dias_atendimento_invalidos(self):
        with self.assertRaises(ValueError):
            DiasAtendimento(lista_dias=[DIAS.SEGUNDA, "TERÇA", DIAS.QUARTA])    