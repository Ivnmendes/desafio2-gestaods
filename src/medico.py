
from datetime import time

class Medico:

    def __init__(self, nome: str, hora_inicio: time, hora_fim: time) -> None:

        if not nome:
            raise ValueError("O médico deve ter nome!")
        
        if not hora_inicio or not hora_fim:
            raise ValueError("O médico deve ter um horário de atendimento")
        
        self._nome = nome
        self._hora_inicio = hora_inicio
        self._hora_fim = hora_fim

    @property
    def nome(self):
        return self._nome
    
    @property
    def hora_inicio(self):
        return self._hora_inicio
    
    @property
    def hora_fim(self):
        return self._hora_fim
    
    def alterar_horario_atendimento(self, hora_inicio: time = None, hora_fim: time = None) -> None:

        self._hora_inicio = hora_inicio if hora_inicio else self._hora_inicio
        
        self._hora_fim = hora_fim if hora_fim else self._hora_fim