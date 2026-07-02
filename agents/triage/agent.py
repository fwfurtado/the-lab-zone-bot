from pathlib import Path

from shared.prompts import load_prompt
from shared.runtime import Assistant

_PROMPT = load_prompt(Path(__file__).parent / "prompts" / "triage.md")

_assistant = Assistant(_PROMPT)

# Contrato AnswerFn consumido pela ponte Slack.
answer = _assistant.answer
