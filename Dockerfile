FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY bot ./bot
COPY agent.py config.py log.py main.py metrics.py ./

RUN pip install .

CMD ["slack-bot"]
