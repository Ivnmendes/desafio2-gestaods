
from datetime import time
from src.utils import DIAS, validar_horario

class Medico:

    def __init__(self, nome: str, hora_inicio: time, hora_fim: time, lista_dias: list[DIAS]) -> None:

        if not nome:
            raise ValueError("O médico deve ter nome!")
        
        if not validar_horario(hora_inicio=hora_inicio, hora_fim=hora_fim):
            raise ValueError("O médico deve ter um horário de atendimento válido!")
        
        if any(dia not in DIAS for dia in lista_dias):
            raise ValueError("Os dias de atendimento devem ser válidos!")
        
        self._nome = nome
        self._hora_inicio = hora_inicio
        self._hora_fim = hora_fim
        self._dias_atendimento = lista_dias

    @property
    def nome(self):
        return self._nome
    
    @property
    def hora_inicio(self):
        return self._hora_inicio
    
    @property
    def hora_fim(self):
        return self._hora_fim
    
    @property
    def dias_atendimento(self):
        return self._dias_atendimento
    
    def alterar_horario_atendimento(self, hora_inicio: time = None, hora_fim: time = None) -> None:

        hora_inicio_alterar = hora_inicio if hora_inicio else self._hora_inicio
        hora_fim_alterar = hora_fim if hora_fim else self._hora_fim

        if not validar_horario(hora_inicio=hora_inicio_alterar, hora_fim=hora_fim_alterar):
            raise ValueError("O médico deve ter um horário de atendimento válido!")
        
        self._hora_inicio = hora_inicio_alterar
        self._hora_fim = hora_fim_alterar

    def alterar_dias_atendimento(self, lista_dias: list[DIAS]) -> None:

        if any(dia not in DIAS for dia in lista_dias):
            raise ValueError("Os dias de atendimento devem ser válidos!")

        self._dias_atendimento = lista_dias
