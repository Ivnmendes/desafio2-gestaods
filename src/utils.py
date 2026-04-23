
from datetime import time, datetime, timedelta

def validar_horario(hora_inicio: time, hora_fim: time) -> bool:

    return hora_inicio is not None and hora_fim is not None and hora_inicio < hora_fim

def gerar_lista_horarios(hora_inicio: time, hora_fim: time, intervalo_minutos: int) -> list[time]:

    horarios = []

    data_atual = datetime.today() # necessario para usar timedelta
    atual_dt = datetime.combine(data_atual, hora_inicio)
    fim_dt = datetime.combine(data_atual, hora_fim)

    passo = timedelta(minutes=intervalo_minutos)

    while atual_dt <= fim_dt:
        horarios.append(atual_dt.time())
        atual_dt += passo

    return horarios