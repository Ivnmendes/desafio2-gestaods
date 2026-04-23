
from enum import Enum
from datetime import time
from typing import Optional, TypedDict
from src.paciente import Paciente
from src.medico import Medico
from src.utils import gerar_lista_horarios

class DIA(Enum):
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"

DURACAO_CONSULTA = 30

class Agendamento(TypedDict):
    horario: time
    paciente: Optional[Paciente]

class Agenda():

    def __init__(self, dia: DIA, medico: Medico):

        self._dia = dia
        self._medico = medico

        list_horarios = gerar_lista_horarios(
            hora_inicio = medico.hora_inicio, 
            hora_fim = medico.hora_fim, 
            intervalo_minutos = DURACAO_CONSULTA
        )

        self._agendamentos = {
            horario: Agendamento(horario=horario, paciente=None)
            for horario in list_horarios
        }

    @property
    def agendamentos(self):
        return self._agendamentos