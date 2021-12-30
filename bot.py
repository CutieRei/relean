import asyncio
import os
from logging import getLogger
from typing import Callable

from discord.ext import commands
from dotenv import load_dotenv


class Relean(commands.Bot):
    def __init__(
        self,
        command_prefix,
        help_command=None,
        description=None,
        logger=None,
        **options,
    ):
        super().__init__(
            command_prefix,
            help_command=help_command or commands.HelpCommand(command_attrs={"aliases": ["halp"]}),
            description=description,
            **options,
        )
        self.logger = logger or getLogger(__name__)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user} in {len(self.guilds)} guilds")

    async def close(self) -> None:
        self.logger.info("Stopping bot")
        await super().close()
        self.logger.info("Bot closed")
        await asyncio.sleep(1)


def get(logger=None) -> tuple[Relean, Callable]:
    load_dotenv()
    token = os.environ["DISCORD_BOT_TOKEN"]

    bot = Relean("rl.", logger=logger)
    bot.load_extension("jishaku")

    return bot, lambda: bot.run(token)
