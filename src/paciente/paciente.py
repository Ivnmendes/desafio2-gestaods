from core.value_objects import Nome


class Paciente:

    def __init__(self, nome: str):

        self._nome = Nome(nome)

    @property
    def nome(self):
        return self._nome.valor
