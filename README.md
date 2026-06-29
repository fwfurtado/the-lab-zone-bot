# the-lab-zone-slack-bot

Bot de Slack para perguntas sobre infra do the-lab-zone.

Ele roda em Socket Mode, consulta um agente com `pydantic-ai` e expõe métricas
Prometheus em `:9090/metrics`.

## Requisitos

- Python 3.12+
- `uv` ou `pip`
- credenciais do Slack
- acesso ao LiteLLM
- acesso ao endpoint ToolHive vMCP

## Variáveis de ambiente

Estas variáveis são obrigatórias:

```bash
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."
export LITELLM_KEY="sk-..."
export TOOLHIVE_VMCP_URL="http://toolhive.example/mcp"
```

Estas variáveis são opcionais:

```bash
export LITELLM_BASE_URL="http://litellm.ai.svc.cluster.local:4000/v1"
export MODEL_NAME="qwen3-coder-30b-local"
export LOG_LEVEL="INFO"
```

## Instalação local

Com `uv`:

```bash
uv sync
```

Com `pip`:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Execução local

Via Python:

```bash
python main.py
```

Via entrypoint instalado:

```bash
slack-bot
```

## Logs

Os logs saem em JSON no stdout. Exemplo:

```json
{"timestamp":"2026-06-29T21:00:00+00:00","level":"INFO","logger":"slack_qa_bot","message":"starting metrics at :9090/metrics"}
```

## Métricas

O processo sobe um servidor HTTP local com métricas Prometheus em:

```text
http://localhost:9090/metrics
```

Métricas expostas hoje:

- `slack_qa_bot_questions_total`
- `slack_qa_bot_answer_errors_total`
- `slack_qa_bot_answer_latency_seconds`

## Docker

Build direto com Docker:

```bash
docker build -t the-lab-zone-slack-bot:latest .
```

Build com `just`:

```bash
just build
```

Tag customizada:

```bash
just build-tag my-image v1
```

Execução:

```bash
docker run --rm \
  -e SLACK_BOT_TOKEN \
  -e SLACK_APP_TOKEN \
  -e LITELLM_KEY \
  -e TOOLHIVE_VMCP_URL \
  -e LITELLM_BASE_URL \
  -e MODEL_NAME \
  -e LOG_LEVEL \
  -p 9090:9090 \
  the-lab-zone-slack-bot:latest
```

## Estrutura

```text
.
├── main.py
├── agent.py
├── config.py
├── log.py
├── metrics.py
└── bot/
    ├── history.py
    ├── message_parser.py
    ├── responder.py
    ├── slack.py
    └── slack_message_updater.py
```
