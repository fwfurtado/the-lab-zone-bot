import asyncio

import logging

from config import get_settings
from metrics import start_metrics_server
from log import configure_logging


logger = logging.getLogger("slack_qa_bot")



def main():
    settings = get_settings()
    from bot.slack import start_bot

    configure_logging(settings.log_level)

    start_metrics_server(port=9090)

    logger.info("starting metrics at :9090/metrics")

    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("finishing app...")


if __name__ == "__main__":
    main()
