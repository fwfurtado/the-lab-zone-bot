import logging
from collections.abc import Sequence

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from shared.config import get_settings
from shared.slack.types import OnDelta

logger = logging.getLogger("the_lab_zone.runtime")


def build_agent(system_prompt: str) -> Agent:
    """Constrói um Agent Pydantic AI ligado ao vMCP e ao modelo via LiteLLM.

    vMCP, LiteLLM e modelo vêm de env (get_settings), então o MESMO código
    serve QA e triagem — cada processo aponta o TOOLHIVE_VMCP_URL pro seu vMCP.
    """
    settings = get_settings()
    toolhive = MCPToolset(settings.toolhive_vmcp_url)
    model = OpenAIChatModel(
        settings.model_name,
        provider=OpenAIProvider(
            base_url=settings.litellm_base_url,
            api_key=settings.litellm_key.get_secret_value(),
        ),
    )
    return Agent(model, toolsets=[toolhive], system_prompt=system_prompt)


class Assistant:
    """Um agente + a lógica de streaming, agnóstico ao domínio.

    A ponte Slack consome `.answer` (contrato shared.slack.types.AnswerFn).
    O que diferencia QA de triagem é só o system prompt injetado no construtor.
    """

    def __init__(self, system_prompt: str) -> None:
        self._agent = build_agent(system_prompt)

    async def answer(
        self,
        question: str,
        history: Sequence[ModelMessage] | None = None,
        on_delta: OnDelta | None = None,
    ) -> str:
        agent = self._agent
        message_history = history or []

        async with agent:
            if on_delta is None:
                result = await agent.run(question, message_history=message_history)
                return result.output

            # Streaming via agent.iter iterando nós — evita o cancelamento de
            # tool call no meio que run_stream+stream_text causava. Não trocar.
            async with agent.iter(
                question,
                message_history=message_history,
            ) as run:
                async for node in run:
                    if agent.is_model_request_node(node):
                        async with node.stream(run.ctx) as stream:
                            async for delta in stream.stream_text(delta=True):
                                if delta:
                                    await on_delta(delta)
                return run.result.output if run.result else ""
