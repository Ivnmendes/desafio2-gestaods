from datetime import time
from unittest import TestCase

from core.utils import Dias
from medico.medico import Medico


class TestMedico(TestCase):

    def test_criar_medico_valido(self):

        medico = Medico(
            nome="Dr House",
            hora_inicio=time(hour=8, minute=0),
            hora_fim=time(hour=12, minute=0),
            lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
        )

        self.assertIsInstance(medico, Medico)
        self.assertEqual("Dr House", medico.nome)
        self.assertEqual(time(hour=8, minute=0), medico.hora_inicio)
        self.assertEqual(time(hour=12, minute=0), medico.hora_fim)
        self.assertEqual(
            [Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
            medico.dias_atendimento,
        )

    def test_nao_criar_medico_hora_invalida(self):

        with self.assertRaises(Exception):
            Medico(
                nome="Dr House",
                hora_inicio=time(hour=-8, minute=0),
                hora_fim=time(hour=12, minute=0),
                lista_dias=[
                    Dias.SEGUNDA,
                    Dias.TERCA,
                    Dias.QUARTA,
                    Dias.QUINTA,
                    Dias.SEXTA,
                ],
            )

    def test_nao_criar_medico_nome_invalido(self):

        with self.assertRaises(ValueError):
            Medico(
                nome="",
                hora_inicio=time(hour=8, minute=0),
                hora_fim=time(hour=12, minute=0),
                lista_dias=[
                    Dias.SEGUNDA,
                    Dias.TERCA,
                    Dias.QUARTA,
                    Dias.QUINTA,
                    Dias.SEXTA,
                ],
            )

    def test_nao_criar_medico_hora_inicio_menor_hora_fim(self):

        with self.assertRaises(ValueError):
            Medico(
                nome="Dr House",
                hora_inicio=time(hour=12, minute=0),
                hora_fim=time(hour=8, minute=0),
                lista_dias=[
                    Dias.SEGUNDA,
                    Dias.TERCA,
                    Dias.QUARTA,
                    Dias.QUINTA,
                    Dias.SEXTA,
                ],
            )

    def test_nao_criar_medico_lista_dias_vazia(self):
        with self.assertRaises(ValueError):
            Medico(
                nome="Dr House",
                hora_inicio=time(hour=8, minute=0),
                hora_fim=time(hour=12, minute=0),
                lista_dias=[],
            )

    def test_nao_criar_medico_lista_dias_invalida(self):
        with self.assertRaises(ValueError):
            Medico(
                nome="Dr House",
                hora_inicio=time(hour=8, minute=0),
                hora_fim=time(hour=12, minute=0),
                lista_dias=[Dias.SEGUNDA, "TERÇA", Dias.QUARTA],
            )

    def test_alterar_horario_atendimento(self):

        medico = Medico(
            nome="Dr House",
            hora_inicio=time(hour=8, minute=0),
            hora_fim=time(hour=12, minute=0),
            lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
        )

        novo_horario_inicio = time(hour=9, minute=30)
        novo_horario_fim = time(hour=13, minute=30)

        medico.alterar_horario_atendimento(novo_horario_inicio, novo_horario_fim)

        self.assertEqual(novo_horario_inicio, medico.hora_inicio)
        self.assertEqual(novo_horario_fim, medico.hora_fim)

    def test_alterar_horario_atendimento_apenas_fim(self):

        medico = Medico(
            nome="Dr House",
            hora_inicio=time(hour=8, minute=0),
            hora_fim=time(hour=12, minute=0),
            lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
        )

        novo_horario_fim = time(hour=13, minute=30)

        medico.alterar_horario_atendimento(hora_fim=novo_horario_fim)

        self.assertEqual(time(hour=8, minute=0), medico.hora_inicio)
        self.assertEqual(novo_horario_fim, medico.hora_fim)

    def test_nao_alterar_horario_atendimento_inicio_depois_do_fim(self):

        medico = Medico(
            nome="Dr House",
            hora_inicio=time(hour=8, minute=0),
            hora_fim=time(hour=12, minute=0),
            lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
        )

        novo_horario_fim = time(hour=7, minute=30)

        with self.assertRaises(ValueError):
            medico.alterar_horario_atendimento(hora_fim=novo_horario_fim)

    def test_alterar_dias_atendimento(self):

        medico = Medico(
            nome="Dr House",
            hora_inicio=time(hour=8, minute=0),
            hora_fim=time(hour=12, minute=0),
            lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
        )

        nova_lista_dias_atendimento = [
            Dias.SEGUNDA,
            Dias.TERCA,
            Dias.QUINTA,
            Dias.SEXTA,
        ]

        medico.alterar_dias_atendimento(lista_dias=nova_lista_dias_atendimento)

        self.assertEqual(nova_lista_dias_atendimento, medico.dias_atendimento)
