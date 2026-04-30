import runpy
from contextlib import redirect_stdout
from datetime import date, datetime, time, timedelta
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

import main
from agenda.agenda import Agenda
from medico.medico import Medico
from paciente.paciente import Paciente


class TestMain(TestCase):

    def test_ui_menu_inicial(self):
        resultado = main.ui_menu_inicial()
        self.assertIn("1 - Criar Agenda", resultado)
        self.assertIn("2 - Listar Agendas", resultado)
        self.assertIn("3 - Marcar Consulta", resultado)
        self.assertIn("4 - Desmarcar Consulta", resultado)
        self.assertIn("5 - Listar Consultas", resultado)
        self.assertIn("0 - Sair", resultado)

    def test_ui_listar_agendas_vazias_e_nao_vazias(self):
        self.assertEqual(main.ui_listar_agendas([]), "Nenhuma agenda disponível.")

        medico = Medico(nome="Dr. Test", hora_inicio=time(9, 0), hora_fim=time(10, 0), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))
        resultado = main.ui_listar_agendas([agenda])
        self.assertIn("Médico: Dr. Test", resultado)

    def test_ui_listar_agendamentos(self):
        self.assertEqual(main.ui_listar_agendamentos(None), "Nenhuma agenda disponível.")

        medico = Medico(nome="Dr. X", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))

        paciente = Paciente(nome="Paciente A")
        data_hora = next(iter(agenda.agendamentos.keys()))
        agenda.agendar_horario(paciente, data_hora)

        listar = main.ui_listar_agendamentos(agenda)
        self.assertIn(data_hora.strftime('%H:%M'), listar)

        todos = main.ui_listar_todos_agendamentos([agenda])
        self.assertIn("Agenda 1:", todos)

    def test_ui_listar_consultas(self):
        self.assertEqual(main.ui_listar_consultas(None), "Nenhuma agenda disponível.")

        medico = Medico(nome="Dr. Y", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))

        self.assertEqual(main.ui_listar_consultas(agenda), "Nenhuma consulta agendada.")

        paciente = Paciente(nome="Paciente B")
        data_hora = next(iter(agenda.agendamentos.keys()))
        agenda.agendar_horario(paciente, data_hora)

        consultas = main.ui_listar_consultas(agenda)
        self.assertIn(paciente.nome, consultas)

    def test_ui_listar_medicos_pacientes(self):
        medicos = [Medico(nome="A", hora_inicio=time(9, 0), hora_fim=time(10, 0), lista_dias=[main.Dias.SEGUNDA])]
        pacientes = [Paciente(nome="P1"), Paciente(nome="P2")]

        m = main.ui_listar_medicos(medicos)
        self.assertIn("Médicos Disponíveis:", m)

        p = main.ui_listar_pacientes(pacientes)
        self.assertIn("Pacientes Disponíveis:", p)

    def test_limpar_tela(self):
        with patch('os.system', return_value=0) as mock_system:
            resultado = main.limpar_tela()

        self.assertIsNone(resultado)
        mock_system.assert_called_once_with('clear')

    def test_selecionar_agenda(self):
        self.assertIsNone(main.selecionar_agenda([]))
        
        medico = Medico(nome="Dr. S", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))

        with patch('builtins.input', return_value='1'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_agenda([agenda])
            self.assertIs(escolha, agenda)

        with patch('builtins.input', return_value='2'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_agenda([agenda])
            self.assertIsNone(escolha)

        with patch('builtins.input', return_value='x'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_agenda([agenda])
            self.assertIsNone(escolha)

    def test_opcao_criar_agenda(self):
        medico = Medico(nome="Dr. C", hora_inicio=time(9, 0), hora_fim=time(10, 0), lista_dias=[main.Dias.SEGUNDA])

        with patch('main.selecionar_medico', return_value=medico):
            with patch('builtins.input', side_effect=['01/04/2026', '05/04/2026']):
                agenda = main.opcao_criar_agenda([medico])
                self.assertIsNotNone(agenda)

        with patch('main.selecionar_medico', return_value=medico):
            with patch('builtins.input', side_effect=['invalid', '05/04/2026']):
                buf = StringIO()
                with redirect_stdout(buf):
                    agenda = main.opcao_criar_agenda([medico])
                self.assertIsNone(agenda)

    def test_opcao_agendar_consulta(self):
        self.assertIsNone(main.opcao_agendar_consulta([], []))

        medico = Medico(nome="Dr. Z", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))
        paciente = Paciente(nome="P3")

        with patch('main.selecionar_agenda', return_value=agenda), patch('main.selecionar_paciente', return_value=paciente):
            dt = next(iter(agenda.agendamentos.keys()))
            date_str = dt.strftime('%d/%m/%Y')
            time_str = dt.strftime('%H:%M')
            with patch('builtins.input', side_effect=[date_str, time_str]):
                buf = StringIO()
                with redirect_stdout(buf):
                    main.opcao_agendar_consulta([agenda], [paciente])
                self.assertIn(paciente, agenda)

        with patch('main.selecionar_agenda', return_value=agenda), patch('main.selecionar_paciente', return_value=paciente):
            with patch('builtins.input', side_effect=['01/01/2000', '00:00']):
                buf = StringIO()
                with redirect_stdout(buf):
                    main.opcao_agendar_consulta([agenda], [paciente])
        
        with patch('main.selecionar_agenda', return_value=agenda), patch('main.selecionar_paciente', return_value=paciente):
            with patch('builtins.input', side_effect=['avc', 'adc']):
                buf = StringIO()
                with redirect_stdout(buf):
                    main.opcao_agendar_consulta([agenda], [paciente])


    def test_opcao_desmarcar_consulta(self):
        self.assertIsNone(main.opcao_desmarcar_consulta([]))

        medico = Medico(nome="Dr. D", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))

        with patch('main.selecionar_agenda', return_value=agenda):
            buf = StringIO()
            with redirect_stdout(buf):
                main.opcao_desmarcar_consulta([agenda])

        paciente = Paciente(nome="P4")
        dt = next(iter(agenda.agendamentos.keys()))
        agenda.agendar_horario(paciente, dt)

        date_str = dt.strftime('%d/%m/%Y')
        time_str = dt.strftime('%H:%M')

        with (
            patch('main.selecionar_agenda', return_value=agenda),
            patch('builtins.input', side_effect=[date_str, time_str]),
            redirect_stdout(StringIO())
        ):
            main.opcao_desmarcar_consulta([agenda])
            self.assertNotIn(paciente, agenda)

    def test_opcao_desmarcar_consulta_exceptions(self):
        
        medico = Medico(nome="Dr. D", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))
        dt = next(iter(agenda.agendamentos.keys()))
        agenda.agendar_horario(Paciente(nome="P1"), dt)

        with (
            patch('main.selecionar_agenda', return_value=agenda),
            patch('builtins.input', side_effect=['avc', 'adc']),
            redirect_stdout(StringIO())
        ):
            main.opcao_desmarcar_consulta([agenda])

        with (
            patch('main.selecionar_agenda', return_value=agenda),
            patch('builtins.input', side_effect=['01/01/2026', '10:00']), 
            redirect_stdout(StringIO())
        ):
            main.opcao_desmarcar_consulta([agenda])

    def test_selecionar_medico(self):
        self.assertIsNone(main.selecionar_medico([]))

        medico = Medico(nome="Dr. M", hora_inicio=time(9, 0), hora_fim=time(10, 0), lista_dias=[main.Dias.SEGUNDA])

        with patch('builtins.input', return_value='1'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_medico([medico])
            self.assertIs(escolha, medico)

        with patch('builtins.input', return_value='2'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_medico([medico])
            self.assertIsNone(escolha)

        with patch('builtins.input', return_value='x'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_medico([medico])
            self.assertIsNone(escolha)
        
    def test_selecionar_paciente(self):
        self.assertIsNone(main.selecionar_paciente([]))

        paciente = Paciente(nome="P5")

        with patch('builtins.input', return_value='1'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_paciente([paciente])
            self.assertIs(escolha, paciente)

        with patch('builtins.input', return_value='2'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_paciente([paciente])
            self.assertIsNone(escolha)

        with patch('builtins.input', return_value='x'):
            buf = StringIO()
            with redirect_stdout(buf):
                escolha = main.selecionar_paciente([paciente])
            self.assertIsNone(escolha)

    def test_main_exit(self):
        with patch('builtins.input', side_effect=['0', '']), patch('os.system', return_value=0):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main()

    def test_main_menu_opcao_criar_agenda(self):
        medico = Medico(nome="Dr. D", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))

        with (
            patch('main.opcao_criar_agenda', return_value=agenda) as mock_criar,
            patch('builtins.input', side_effect=['1', '', '0', '']),
            patch('os.system', return_value=0),
        ):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main([])

        mock_criar.assert_called_once()
        self.assertIn('Agenda criada com sucesso!', buf.getvalue())

    def test_main_menu_opcao_listar_agendas(self):
        medico = Medico(nome="Dr. D", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))
        
        with (
            patch('main.ui_listar_todos_agendamentos', return_value='') as mock_listar,
            patch('builtins.input', side_effect=['2', '', '0', '']),
            patch('os.system', return_value=0),
        ):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main(agenda)

        mock_listar.assert_called_once()

    def test_main_menu_opcao_agendar_consulta(self):
        medico = Medico(nome="Dr. D", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))

        with (
            patch('main.opcao_agendar_consulta') as mock_agendar,
            patch('builtins.input', side_effect=['3', '', '0', '']),
            patch('os.system', return_value=0),
        ):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main(agenda)

        mock_agendar.assert_called_once()

    def test_main_menu_opcao_desmarcar_consulta(self):
        medico = Medico(nome="Dr. D", hora_inicio=time(9, 0), hora_fim=time(9, 30), lista_dias=[main.Dias.SEGUNDA])
        agenda = Agenda(medico, date(2026, 4, 6), date(2026, 4, 6))

        with (
            patch('main.opcao_desmarcar_consulta') as mock_desmarcar,
            patch('builtins.input', side_effect=['4', '', '0', '']),
            patch('os.system', return_value=0),
        ):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main(agenda)

        mock_desmarcar.assert_called_once()

    def test_main_menu_opcao_listar_consultas(self):
        agenda = Agenda(
            Medico(nome='Dr. Menu', hora_inicio=time(9, 0), hora_fim=time(10, 0), lista_dias=[main.Dias.SEGUNDA]),
            date(2026, 4, 6),
            date(2026, 4, 6),
        )

        with (
            patch('main.selecionar_agenda', return_value=agenda) as mock_selecionar,
            patch('main.ui_listar_consultas', return_value='CONSULTAS') as mock_listar,
            patch('builtins.input', side_effect=['5', '', '0', '']),
            patch('os.system', return_value=0),
        ):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main(agenda)

        mock_selecionar.assert_called_once()
        mock_listar.assert_called_once_with(agenda)
        self.assertIn('CONSULTAS', buf.getvalue())

    def test_main_menu_opcao_invalida(self):
        with (
            patch('builtins.input', side_effect=['9', '', '0', '']),
            patch('os.system', return_value=0),
        ):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main()

        self.assertIn('Opção inválida. Tente novamente.', buf.getvalue())

    def test_main_menu_sem_agendas(self):

        with (
            patch('builtins.input', side_effect=['3', '4', '5', '0', '']),
            patch('os.system', return_value=0),
        ):
            buf = StringIO()
            with redirect_stdout(buf):
                main.main()

        saida = buf.getvalue()
        self.assertIn('Crie uma agenda primeiro!', saida)

    def test_main_executar(self):
        with (
            patch('builtins.input', side_effect=['0', '']),
            patch('os.system', return_value=0),
            patch('sys.stdout', new=StringIO())
        ):
            runpy.run_module('main', run_name='__main__')