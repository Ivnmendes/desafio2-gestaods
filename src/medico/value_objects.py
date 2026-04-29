from datetime import time

from src.core.utils import Dias, validar_horario


class IntervaloHorario:

    def __init__(self, hora_inicio: time, hora_fim: time):

        if not validar_horario(hora_inicio=hora_inicio, hora_fim=hora_fim):
            raise ValueError("O médico deve ter um horário de atendimento válido!")

        self._hora_inicio = hora_inicio
        self._hora_fim = hora_fim

    @property
    def hora_inicio(self):
        return self._hora_inicio

    @property
    def hora_fim(self):
        return self._hora_fim


class DiasAtendimento:

    def __init__(self, lista_dias: list[Dias]):

        if len(lista_dias) == 0:
            raise ValueError("O médico deve ter pelo menos um dia de atendimento!")
        
        valores_validos = {d.value for d in Dias}
        if any((dia.value if isinstance(dia, Dias) else dia) not in valores_validos for dia in lista_dias):
            raise ValueError("Os dias de atendimento devem ser válidos!")

        self._lista_dias = lista_dias

    @property
    def valor(self):
        return self._lista_dias
