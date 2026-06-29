import time


_STREAM_THROTTLE_S = 0.8


class SlackMessageUpdater:
    """
    Atualiza uma mensagem do Slack incrementalmente, com throttle.
    """

    def __init__(self, logger, client, channel: str, ts: str):
        self._logger = logger
        self._client = client
        self._channel = channel
        self._ts = ts
        self._buffer = ""
        self._last_update = 0.0
        self._dirty = False

    async def push(self, delta: str) -> None:
        self._buffer += delta
        self._dirty = True
        now = time.monotonic()
        if now - self._last_update >= _STREAM_THROTTLE_S:
            await self._flush()

    async def _flush(self) -> None:
        if not self._dirty or not self._buffer:
            return

        try:
            await self._client.chat_update(
                channel=self._channel,
                ts=self._ts,
                text=self._buffer,
            )
            self._last_update = time.monotonic()
            self._dirty = False
        except Exception:
            self._logger.debug(
                "chat_update intermediario falhou; tentando no flush final.",
                exc_info=True,
            )

    async def finalize(self, text: str | None = None) -> None:
        if text is not None:
            self._buffer = text
            self._dirty = True

        self._last_update = 0.0
        await self._flush()
