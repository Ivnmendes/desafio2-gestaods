
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

    def __contains__(self, paciente: Paciente) -> bool:
        for agendamento in self._agendamentos.values():
            if agendamento['paciente'] == paciente:
                return True
        return False
    
    def __len__(self) -> int:
        count = 0
        for agendamento in self._agendamentos.values():
            if agendamento['paciente'] is not None:
                count += 1

        return count
    
    @property
    def agendamentos(self) -> Agendamento:
        return self._agendamentos
    
    @property
    def medico(self) -> Medico:
        return self._medico
    
    @property
    def dia(self) -> DIA:
        return self._dia
    
    def agendar_horario(self, paciente: Paciente, horario: time) -> None:

        if not self.verificar_horario_disponivel(horario):
            raise Exception("Horário ocupado/inexistente, escolha outro!")
        
        self._agendamentos[horario]['paciente'] = paciente

    def desmarcar_horario(self, horario: time) -> None:

        if not horario in self._agendamentos.keys():
            raise Exception("Horário não coberto pelo médico!")
            
        self._agendamentos[horario]['paciente'] = None

    def verificar_horario_disponivel(self, horario: time) -> bool:

        if not horario in self._agendamentos.keys():
            return False

        return self._agendamentos[horario]['paciente'] is None