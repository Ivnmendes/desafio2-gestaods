
class Paciente:

    def __init__(self, nome: str):

        if not nome:
            raise ValueError("O paciente deve ter um nome!")
        
        self._nome = nome

    @property
    def nome(self):
        return self._nome