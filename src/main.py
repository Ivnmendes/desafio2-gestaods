import os
from datetime import date, datetime, time
from itertools import groupby

from agenda.agenda import Agenda
from core.exceptions import HorarioIndisponivelException
from core.utils import MAPA_DIAS_SEMANA, Dias
from medico.medico import Medico
from paciente.paciente import Paciente


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def ui_menu_inicial() -> str:
    return """
    1 - Criar Agenda
    2 - Listar Agendas
    3 - Marcar Consulta
    4 - Desmarcar Consulta
    5 - Listar Consultas
    0 - Sair
    """


def ui_listar_agendas(agendas: list[Agenda]) -> str:

    if len(agendas) == 0:
        return "Nenhuma agenda disponível."

    resultado = ""
    for i, agenda in enumerate(agendas):
        resultado += (
            f"{i + 1} - Médico: {agenda.medico.nome}, "
            f"Total de Agendamentos: {len(agenda)}\n"
        )

    return resultado


def ui_listar_agendamentos(agenda: Agenda) -> str:

    if agenda is None:
        return "Nenhuma agenda disponível."

    resultado = ""

    for data, grupo in groupby(agenda.agendamentos.items(), key=lambda x: x[0].date()):

        dia_semana = MAPA_DIAS_SEMANA[data.weekday()]

        resultado += f"\n--- {data.strftime('%d/%m/%Y')} ({dia_semana}) ---\n"

        for data_hora, agendamento in grupo:
            paciente_nome = (
                agendamento["paciente"].nome
                if agendamento["paciente"]
                else "Disponível"
            )
            resultado += f"  {data_hora.strftime('%H:%M')} - {paciente_nome}\n"

    return resultado


def ui_listar_todos_agendamentos(lista_agendas: list[Agenda]) -> str:

    resultado = ""
    for i, agenda in enumerate(lista_agendas):
        resultado += "-" * 30 + "\n"
        resultado += (
            f"Agenda {i + 1}:"
            f" Médico: {agenda.medico.nome}, "
            f"Total de Agendamentos: {len(agenda)}\n"
        )
        resultado += ui_listar_agendamentos(agenda)
        resultado += "-" * 30 + "\n"

    return resultado


def ui_listar_consultas(agenda: Agenda) -> str:

    if agenda is None:
        return "Nenhuma agenda disponível."

    resultado = ""

    for data_hora, agendamento in agenda.agendamentos.items():
        if agendamento["paciente"] is not None:
            resultado += (
                f"{data_hora.strftime('%d/%m/%Y %H:%M')} - "
                f"Paciente: {agendamento['paciente'].nome}\n"
            )

    return resultado if resultado else "Nenhuma consulta agendada."


def ui_listar_medicos(medicos: list[Medico]) -> str:

    resultado = "Médicos Disponíveis:\n"
    for i, medico in enumerate(medicos):
        resultado += f"{i + 1} - {medico.nome}\n"

    return resultado


def ui_listar_pacientes(pacientes: list[Paciente]) -> str:

    resultado = "Pacientes Disponíveis:\n"
    for i, paciente in enumerate(pacientes):
        resultado += f"{i + 1} - {paciente.nome}\n"

    return resultado


def selecionar_agenda(agendas: list[Agenda]) -> Agenda | None:

    if len(agendas) == 0:
        print("Nenhuma agenda disponível.")
        return None

    print("Selecione uma agenda:")
    print(ui_listar_agendas(agendas))
    opcao = input("Escolha uma opção: ")
    try:
        opcao_int = int(opcao)
        if 1 <= opcao_int <= len(agendas):
            return agendas[opcao_int - 1]
        else:
            print("Opção inválida. Tente novamente.")
            return None
    except ValueError:
        print("Opção inválida. Tente novamente.")
        return None


def selecionar_paciente(pacientes: list[Paciente]) -> Paciente | None:

    if len(pacientes) == 0:
        print("Nenhum paciente disponível.")
        return None

    print("Selecione um paciente:")
    print(ui_listar_pacientes(pacientes))
    opcao = input("Escolha uma opção: ")
    try:
        opcao_int = int(opcao)
        if 1 <= opcao_int <= len(pacientes):
            return pacientes[opcao_int - 1]
        else:
            print("Opção inválida. Tente novamente.")
            return None
    except ValueError:
        print("Opção inválida. Tente novamente.")
        return None


def selecionar_medico(medicos: list[Medico]) -> Medico | None:

    if len(medicos) == 0:
        print("Nenhum médico disponível.")
        return None

    print("Selecione um médico:")
    print(ui_listar_medicos(medicos))
    opcao = input("Escolha uma opção: ")
    try:
        opcao_int = int(opcao)
        if 1 <= opcao_int <= len(medicos):
            return medicos[opcao_int - 1]
        else:
            print("Opção inválida. Tente novamente.")
            return None
    except ValueError:
        print("Opção inválida. Tente novamente.")
        return None


def opcao_criar_agenda(lista_medicos: list[Medico]) -> Agenda | None:

    medico = selecionar_medico(lista_medicos)

    try:

        print("Insira a data inicial da agenda (DD/MM/AAAA): ")
        dia_i, mes_i, ano_i = input().split("/")
        print("Insira a data final da agenda (DD/MM/AAAA): ")
        data_final = input().split("/")
        dia_f, mes_f, ano_f = data_final

        agenda = Agenda(
            medico,
            date(int(ano_i), int(mes_i), int(dia_i)),
            date(int(ano_f), int(mes_f), int(dia_f)),
        )

        return agenda

    except ValueError:

        print("Data inválida. Tente novamente.")
        return None

    except Exception as e:

        print(f"Erro ao criar agenda: {e}")
        return None


def opcao_agendar_consulta(
    lista_agendas: list[Agenda], lista_pacientes: list[Paciente]
) -> None:

    agenda = selecionar_agenda(lista_agendas)
    paciente = selecionar_paciente(lista_pacientes)

    if agenda is None or paciente is None:
        return

    print(ui_listar_agendamentos(agenda))

    try:
        print("Insira a data da consulta (DD/MM/AAAA): ")
        dia, mes, ano = input().split("/")
        print("Insira a hora da consulta (HH:MM): ")
        hora, minuto = input().split(":")
        data_hora = datetime(int(ano), int(mes), int(dia), int(hora), int(minuto))

        agenda.agendar_horario(paciente, data_hora)
        print("Consulta agendada com sucesso!")

    except ValueError:
        print("Data ou hora inválida. Tente novamente.")

    except HorarioIndisponivelException as e:
        print(f"Horário indisponível: {e}")

    except Exception as e:
        print(f"Erro ao agendar consulta: {e}")


def opcao_desmarcar_consulta(lista_agendas: list[Agenda]) -> None:

    agenda = selecionar_agenda(lista_agendas)

    if agenda is None:
        return

    if len(agenda) == 0:
        print("Nenhuma consulta agendada para desmarcar.")
        return

    print(ui_listar_consultas(agenda))

    try:
        print("Insira a data da consulta a ser desmarcada (DD/MM/AAAA): ")
        dia, mes, ano = input().split("/")
        print("Insira a hora da consulta a ser desmarcada (HH:MM): ")
        hora, minuto = input().split(":")
        data_hora = datetime(int(ano), int(mes), int(dia), int(hora), int(minuto))

        agenda.desmarcar_horario(data_hora)
        print("Consulta desmarcada com sucesso!")

    except ValueError:
        print("Data ou hora inválida. Tente novamente.")

    except HorarioIndisponivelException as e:
        print(f"Horário indisponível: {e}")

    except Exception as e:
        print(f"Erro ao desmarcar consulta: {e}")


def main():

    medico = Medico(
        nome="Dr. House",
        hora_inicio=time(9, 0),
        hora_fim=time(17, 0),
        lista_dias=[Dias.SEGUNDA, Dias.TERCA, Dias.QUARTA, Dias.QUINTA, Dias.SEXTA],
    )
    paciente_1 = Paciente(nome="Foremann")
    paciente_2 = Paciente(nome="Chase")

    lista_medicos = [medico]
    lista_pacientes = [paciente_1, paciente_2]
    lista_agendas = [Agenda(medico, date(2026, 4, 1), date(2026, 4, 5))]

    flag_rodar = True

    while flag_rodar:

        print(limpar_tela())
        print(ui_menu_inicial())
        opcao = input("Escolha uma opção: ")

        print(limpar_tela())
        if opcao == "1":
            agenda = opcao_criar_agenda(lista_medicos)

            if agenda is not None:
                lista_agendas.append(agenda)
                print("Agenda criada com sucesso!")

        if opcao == "2":
            print(ui_listar_todos_agendamentos(lista_agendas))

        elif opcao == "3":
            if len(lista_agendas) == 0:
                print("Crie uma agenda primeiro!")
                continue

            opcao_agendar_consulta(lista_agendas, lista_pacientes)

        elif opcao == "4":
            if len(lista_agendas) == 0:
                print("Crie uma agenda primeiro!")
                continue

            opcao_desmarcar_consulta(lista_agendas)

        elif opcao == "5":
            if len(lista_agendas) == 0:
                print("Crie uma agenda primeiro!")
                continue

            agenda = selecionar_agenda(lista_agendas)

            if agenda is not None:
                print(ui_listar_consultas(agenda))

        elif opcao == "0":
            flag_rodar = False
        else:
            print("Opção inválida. Tente novamente.")

        print("Pressione Enter para continuar...")
        input()


if __name__ == "__main__":
    main()
