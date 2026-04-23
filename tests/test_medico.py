
from unittest import TestCase
from src.medico import Medico
from datetime import time

class TestMedico(TestCase):

    def test_criar_medico_valido(self):

        medico = Medico(
            nome = "Dr House",
            hora_inicio = time(
                hour = 8,
                minute = 0
            ),
            hora_fim = time(
                hour = 12,
                minute = 0
            )
        )

        self.assertIsInstance(medico, Medico)

    def test_nao_criar_medico_hora_invalida(self):

        with self.assertRaises(Exception):
            medico = Medico(
            nome = "Dr House",
            hora_inicio = time(
                hour = -8,
                minute = 0
            ),
            hora_fim = time(
                hour = 12,
                minute = 0
            )
        )
            
    def test_nao_criar_medico_nome_invalido(self):

        with self.assertRaises(ValueError):
            medico = Medico(
            nome = "",
            hora_inicio = time(
                hour = 8,
                minute = 0
            ),
            hora_fim = time(
                hour = 12,
                minute = 0
            )
        )
            
    def test_alterar_horario_atendimento(self):

        medico = Medico(
            nome = "Dr House",
            hora_inicio = time(
                hour = 8,
                minute = 0
            ),
            hora_fim = time(
                hour = 12,
                minute = 0
            )
        )

        novo_horario_inicio = time(
            hour = 9,
            minute = 30
        )
        novo_horario_fim = time(
            hour = 13,
            minute = 30
        )

        medico.alterar_horario_atendimento(novo_horario_inicio, novo_horario_fim)

        self.assertEqual(novo_horario_inicio, medico.hora_inicio)
        self.assertEqual(novo_horario_fim, medico.hora_fim)

    def test_alterar_horario_atendimento_apenas_fim(self):

        medico = Medico(
            nome = "Dr House",
            hora_inicio = time(
                hour = 8,
                minute = 0
            ),
            hora_fim = time(
                hour = 12,
                minute = 0
            )
        )

        novo_horario_fim = time(
            hour = 13,
            minute = 30
        )

        medico.alterar_horario_atendimento(hora_fim = novo_horario_fim)

        self.assertEqual(time(
            hour=8,
            minute=0
        ), medico.hora_inicio)
        self.assertEqual(novo_horario_fim, medico.hora_fim)
