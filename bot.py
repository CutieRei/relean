import asyncio
import os
from logging import getLogger
from typing import Callable
import discord
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
            help_command=help_command
            or commands.HelpCommand(command_attrs={"aliases": ["halp"]}),
            description=description,
            **options,
        )
        self.logger = logger or getLogger(__name__)

    async def on_ready(self):
        self.logger.info(
            f"Logged in as {self.user}[{self.user.id}] in {len(self.guilds)} guilds"
        )

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

    @bot.command()
    @commands.is_owner()
    async def restart(ctx):
        async def _restart():
            await bot.close()
            with open(".state", "w") as f:
                f.writelines([str(ctx.channel.id) + "\n", str(ctx.message.id)])

        await ctx.reply("Scheduled restart")
        asyncio.create_task(_restart())

    async def start():
        async def _check_restart():
            await bot.wait_until_ready()
            if not os.path.isfile(".state"):
                return
            with open(".state", "r+") as f:
                channel, message = [int(i.strip()) for i in f.readlines()]
            channel = bot.get_partial_messageable(
                channel, type=discord.ChannelType.text
            )
            message = channel.get_partial_message(message)
            os.remove(".state")
            await message.reply("Restart success")

        asyncio.create_task(_check_restart())
        await bot.start(token)

    return bot, start
