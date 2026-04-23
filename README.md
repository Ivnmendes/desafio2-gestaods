# Módulo de Agendamento Inteligente (MVP)

Este projeto é uma solução de backend em Python focada na automação e validação de agendas médicas. O objetivo principal é eliminar erros manuais de sobreposição e agendamentos fora do turno, reduzindo o churn e a carga operacional das clínicas.

## O Problema

Atualmente, as clínicas parceiras enfrentam:

* **22% do tempo das secretárias** desperdiçado com renegociações.
* **15% de erro manual** com sobreposição de horários.
* **Prejuízo estimado de R$ 5.000/mês** por furos na agenda.

## Solução Proposta

O módulo automatiza a validação de regras de negócio críticas:

1.**Configuração de Grade:** Definição rigorosa da jornada do médico.

2.**Validação de Horário:** Bloqueio automático de consultas fora do turno.

3.**Prevenção de Sobreposição:** Verificação de conflitos para garantir agenda única por horário.

## Tecnologias Utilizadas

* **Linguagem:** Python 3.x

* **Testes:** `unittest` (Standard Library)

## Testes e Qualidade

Para garantir a confiabilidade do sistema e o cumprimento dos **Critérios de Aceitação** definidos no PRD, foram implementados testes automatizados cobrindo os seguintes cenários:

* ✅ **Sucesso:** Agendamento dentro do horário e sem conflitos.
* ❌ **Erro de Disponibilidade:** Tentativa de agendamento fora do turno do médico.
* ❌ **Erro de Conflito:** Tentativa de sobreposição de horários.

### Como rodar os testes

No terminal, execute o comando abaixo na raiz do projeto:

```bash
python -m unittest discover -s tests -t . -v
```
