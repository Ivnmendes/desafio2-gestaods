class Nome:

    def __init__(self, nome: str):

        if not nome or not nome.strip():
            raise ValueError("O nome não pode ser vazio")

        self._valor = nome

    @property
    def valor(self) -> str:
        return self._valor
