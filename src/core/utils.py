from datetime import date, datetime, time, timedelta
from enum import Enum


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
