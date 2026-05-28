# ArrhythmiaMonitor
Sistema de monitoramento cardíaco inteligente com detecção de arritmias (simuladas) em tempo real, integrado à Azure com modelo Random Forest, API FastAPI e dashboard interativo.


# Relatório de Especificação — Agente CardioMonitor
**Destinatário:** Desenvolvedor do agente
**Projeto:** Care Plus / CardioMonitor
**Data:** 28/05/2026

---

## ⚠️ Escopo Obrigatório — Leia Primeiro

Este agente **NÃO é um assistente de saúde geral**.
Ele é restrito exclusivamente a temas **cardiovasculares e do sistema
circulatório**. Qualquer pergunta fora desse escopo deve ser recusada
educadamente, redirecionando o usuário para um profissional adequado.

**Não responder sobre:** oncologia, ortopedia, dermatologia,
saúde mental, nutrição geral, ou qualquer condição não cardiovascular.

O agente **nunca diagnostica definitivamente** — sempre finaliza
recomendando avaliação médica presencial.

---

## 1. Modelo

Utilizar **Qwen** como modelo base do agente.

---

## 2. Base de Conhecimento (RAG)

Os arquivos `.md` já existem no repositório do projeto anterior.
Todos devem ser carregados como contexto do agente:

- `anti_coagulante_bula_resumida.md`
- `anti_hipertensivos_bula_resumida.md`
- `cartilha_beneficiario_saude_cardiaca.md`
- `diretrizes_sbc_hipertensao_arritmia.md`
- `politicas_care_plus_telemedicina.md`
- `protocolo_triagem_cardiovascular.md`
- `red_flags_cardiovasculares.md`

Esses arquivos são a fonte primária de respostas sobre medicamentos,
diretrizes clínicas, protocolos e orientações ao beneficiário.
O agente deve priorizar essas fontes antes de usar conhecimento
geral do modelo.

---

## 3. Funcionalidades Esperadas

### 3.1 Agendamento de Consultas

O agente deve ser capaz de marcar consultas com o Dr. Gregory House
a pedido do usuário via chat.

**Fluxo:**
1. Usuário solicita agendamento no chat
2. Agente coleta data, horário e motivo da consulta
3. Agente salva a consulta em `consultas_gabriel.json` no
   Blob Storage (`container: dataset`)
4. O arquivo deve ser criado automaticamente caso não exista —
   padrão "cria se não existir"
5. O `gabriel.py` já está preparado para ler esse arquivo e exibir
   a nova consulta no HUD de "Próximas Consultas"

**Credenciais:** usar a variável de ambiente
`AZURE_STORAGE_CONNECTION_STRING` já presente no `.env` do projeto.
O Blob funciona local — deploy não é pré-requisito.

**Estrutura sugerida de cada entrada no JSON:**
```json
{
  "data": "DD/MM/AAAA",
  "tipo": "Consulta agendada via agente",
  "medico": "Dr. Gregory House",
  "resumo": "Motivo informado pelo usuário",
  "status": "agendada"
}
```

### 3.2 Relatório de Registros Recentes

A pedido do usuário, o agente deve buscar os registros mais recentes
do Blob Storage e devolver um relatório em linguagem natural.

**Fluxo:**
1. Usuário pede um relatório ("como estão meus últimos registros?")
2. Agente chama `load_blob(tail=50)` — função já existente em
   `dashboard/utils/storage.py`
3. Agente monta um prompt com os dados (IBI, BPM, desvio_medio,
   bat_anormais, status) e envia ao modelo
4. Modelo devolve análise em linguagem natural com:
   - Frequência cardíaca média e variação
   - Predominância de status (regular / atenção / irregular)
   - Inferência do tipo de arritmia pela assinatura do IBI:
     - IBIs curtos e regulares → taquicardia
     - IBIs longos e regulares → bradicardia
     - IBIs caóticos → fibrilação atrial
     - IBI curto seguido de pausa longa → extrassístole
   - Recomendação final de avaliação médica (obrigatório)

### 3.3 Dúvidas sobre Medicamentos e Diretrizes

O agente responde perguntas sobre os medicamentos do paciente
(Warfarina, Atenolol, Losartana) e orientações cardiovasculares
gerais usando os `.md` como fonte.

Exemplos de perguntas esperadas:
- "Posso tomar ibuprofeno junto com a Warfarina?"
- "Quais os sinais de sangramento que devo observar?"
- "O que é o escore CHA₂DS₂-VA?"

---

## 4. Restrições de Comportamento

- Nunca emitir diagnóstico definitivo
- Nunca orientar suspender medicamento sem médico
- Sempre finalizar respostas clínicas com recomendação de
  avaliação presencial
- Recusar perguntas fora do escopo cardiovascular/circulatório
- Não inventar informações não presentes nos `.md`

---

## 5. Integração com o Dashboard

O agente será exibido em uma aba de chat dentro do dashboard Dash.
A aba já está prevista no projeto. A integração com o Blob
(leitura de registros e escrita de consultas) deve usar a mesma
`AZURE_STORAGE_CONNECTION_STRING` do restante do sistema.

---

## 6. Memória do Agente

Utilizar memória de **sessão** — o agente mantém o contexto da
conversa enquanto o dashboard estiver aberto, zerando ao fechar.

Implementar via `dcc.Store(storage_type="session")`, padrão já
adotado no `monitor.py` do projeto.

O histórico clínico persistente (consultas, medicamentos,
diagnóstico) já é fornecido a cada sessão via RAG e Blob —
memória permanente de chat não é necessária. Informações
importantes registradas pelo usuário devem ser salvas via
agendamento de consulta.

---
*Documento interno — Care Plus / CardioMonitor — fins acadêmicos.*