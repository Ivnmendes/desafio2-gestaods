from __future__ import annotations

from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import TYPE_CHECKING


class DIAS(Enum):
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"
    SABADO = "sabado"
    DOMINGO = "domingo"


MAPA_DIAS_SEMANA = {
    DIAS.SEGUNDA: 0,
    DIAS.TERCA: 1,
    DIAS.QUARTA: 2,
    DIAS.QUINTA: 3,
    DIAS.SEXTA: 4,
    DIAS.SABADO: 5,
    DIAS.DOMINGO: 6,
}


def validar_horario(hora_inicio: time, hora_fim: time) -> bool:

    return hora_inicio is not None and hora_fim is not None and hora_inicio < hora_fim


def gerar_lista_horarios(
    hora_inicio: time, hora_fim: time, intervalo_minutos: int
) -> list[time]:

    horarios = []

    data_atual = date.min  # necessario para usar timedelta
    atual_dt = datetime.combine(data_atual, hora_inicio)
    fim_dt = datetime.combine(data_atual, hora_fim)

    passo = timedelta(minutes=intervalo_minutos)

    while atual_dt <= fim_dt:
        horarios.append(atual_dt.time())
        atual_dt += passo

    return horarios


if TYPE_CHECKING:
    from src.medico.medico import Medico


def gerar_lista_datetime(
    medico: Medico,
    data_inicio: date,
    data_fim: date,
    intervalo_minutos: int,
) -> list[datetime]:

    dias = []

    dias_trabalho_ints = [
        MAPA_DIAS_SEMANA[dia_enum] for dia_enum in medico.dias_atendimento
    ]

    dia_atual = data_inicio
    while dia_atual <= data_fim:

        if dia_atual.weekday() in dias_trabalho_ints:

            horarios_do_dia = gerar_lista_horarios(
                hora_inicio=medico.hora_inicio,
                hora_fim=medico.hora_fim,
                intervalo_minutos=intervalo_minutos,
            )

            for horario in horarios_do_dia:
                novo_slot = datetime.combine(dia_atual, horario)
                dias.append(novo_slot)

        dia_atual += timedelta(days=1)

    return dias
