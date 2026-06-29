"""
metrics.py — métricas Prometheus do slack-qa-bot.

Expostas pra VictoriaMetrics raspar (VMPodScrape). Meta-observabilidade: o bot
que responde sobre a infra também é observado pela mesma stack.
"""

from prometheus_client import Counter, Histogram, start_http_server

questions_total = Counter(
    "slack_qa_bot_questions_total",
    "Total de perguntas recebidas pelo bot.",
)

answer_errors_total = Counter(
    "slack_qa_bot_answer_errors_total",
    "Total de perguntas que falharam ao responder.",
)

answer_latency = Histogram(
    "slack_qa_bot_answer_latency_seconds",
    "Latência de responder uma pergunta, do recebimento ao texto final.",
    buckets=(0.5, 1, 2, 5, 10, 20, 30, 60, 120),
)


def start_metrics_server(port: int = 9090) -> None:
    start_http_server(port)
