
from datetime import time
from src.core.utils import DIAS, validar_horario
from src.core.value_objects import Nome
from src.medico.value_objects import DiasAtendimento, IntervaloHorario

class Medico:

    def __init__(self, nome: str, hora_inicio: time, hora_fim: time, lista_dias: list[DIAS]) -> None:
        
        self._nome = Nome(nome = nome)
        self._intervalo_horarios = IntervaloHorario(hora_inicio = hora_inicio, hora_fim = hora_fim)
        self._dias_atendimento = DiasAtendimento(lista_dias = lista_dias)

    @property
    def nome(self):
        return self.nome.valor
    
    @property
    def hora_inicio(self):
        return self._intervalo_horarios.hora_inicio
    
    @property
    def hora_fim(self):
        return self._intervalo_horarios.hora_fim
    
    @property
    def dias_atendimento(self):
        return self._dias_atendimento.valor
    
    def alterar_horario_atendimento(self, hora_inicio: time = None, hora_fim: time = None) -> None:

        hora_inicio_alterar = hora_inicio if hora_inicio else self.hora_inicio
        hora_fim_alterar = hora_fim if hora_fim else self.hora_fim

        self._intervalo_horarios = IntervaloHorario(hora_inicio = hora_inicio_alterar, hora_fim = hora_fim_alterar)

    def alterar_dias_atendimento(self, lista_dias: list[DIAS]) -> None:

        self._dias_atendimento = DiasAtendimento(lista_dias = lista_dias)
