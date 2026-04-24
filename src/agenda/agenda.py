from datetime import date, datetime
from typing import Optional, TypedDict

from src.core.exceptions import HorarioIndisponivelException
from src.core.utils import gerar_lista_datetime
from src.medico.medico import Medico
from src.paciente.paciente import Paciente

DURACAO_CONSULTA = 30


class Agendamento(TypedDict):
    data_hora: datetime
    paciente: Optional[Paciente]


class Agenda:

    def __init__(self, medico: "Medico", data_inicio: date, data_fim: date):

        self._medico = medico

        if data_inicio > data_fim:
            raise ValueError("A data inicial deve ser menor que a data final!")

        lista_datetimes = gerar_lista_datetime(
            medico, data_inicio, data_fim, DURACAO_CONSULTA
        )

        self._agendamentos = {
            dt: Agendamento(data_hora=dt, paciente=None) for dt in lista_datetimes
        }

    def __contains__(self, paciente: Paciente) -> bool:
        for agendamento in self._agendamentos.values():
            if agendamento["paciente"] == paciente:
                return True
        return False

    def __len__(self) -> int:
        count = 0
        for agendamento in self._agendamentos.values():
            if agendamento["paciente"] is not None:
                count += 1

        return count

    @property
    def agendamentos(self) -> dict[datetime, Agendamento]:
        return self._agendamentos

    @property
    def medico(self) -> Medico:
        return self._medico

    def agendar_horario(self, paciente: "Paciente", data_hora: datetime) -> None:

        if not self.verificar_horario_disponivel(data_hora):
            raise HorarioIndisponivelException(
                "Horário ocupado/inexistente, escolha outro!"
            )

        self._agendamentos[data_hora]["paciente"] = paciente

    def desmarcar_horario(self, data_hora: datetime) -> None:

        if data_hora not in self._agendamentos.keys():
            raise HorarioIndisponivelException("Horário não coberto pelo médico!")

        self._agendamentos[data_hora]["paciente"] = None

    def verificar_horario_disponivel(self, data_hora: datetime) -> bool:

        if data_hora not in self._agendamentos.keys():
            return False

        return self._agendamentos[data_hora]["paciente"] is None
