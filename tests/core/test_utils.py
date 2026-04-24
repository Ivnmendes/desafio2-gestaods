from datetime import time
from unittest import TestCase

from src.core.utils import gerar_lista_horarios, validar_horario

class TestUtils(TestCase):

    def test_validar_horarios_valido(self):

        resultado = validar_horario(
            hora_inicio = time(
                hour = 9,
                minute = 30
            ),
            hora_fim = time(
                hour = 10,
                minute = 30
            )
        )

        self.assertTrue(resultado)

    def test_validar_horarios_invalido(self):

        resultado = validar_horario(
            hora_inicio = time(
                hour = 9,
                minute = 30
            ),
            hora_fim = time(
                hour = 8,
                minute = 30
            )
        )

        self.assertFalse(resultado)

    def test_gerar_lista_horarios(self):

        lista_horarios = gerar_lista_horarios(
            hora_inicio = time(
                hour = 8,
                minute = 30
            ),
            hora_fim = time(
                hour = 10,
                minute = 30
            ),
            intervalo_minutos = 30
        )

        lista_esperada = [
            time(8, 30),
            time(9, 0),
            time(9, 30),
            time(10, 0),
            time(10, 30)
        ]

        self.assertEqual(lista_esperada, lista_horarios)

    def test_gerar_lista_horarios_horario_invalido(self):

        lista_horarios = gerar_lista_horarios(
            hora_inicio = time(
                hour = 8,
                minute = 30
            ),
            hora_fim = time(
                hour = 7,
                minute = 30
            ),
            intervalo_minutos = 30
        )

        lista_esperada = [
        ]

        self.assertEqual(lista_esperada, lista_horarios)