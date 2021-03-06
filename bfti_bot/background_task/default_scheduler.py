from __future__ import annotations

from asyncio import sleep
from inspect import iscoroutinefunction
from logging import getLogger
from typing import TYPE_CHECKING

from .task import Scheduler, Task

if TYPE_CHECKING:
    from ..bot import Bot

log = getLogger('default_scheduler')


class DefaultScheduler(Scheduler):
    """Simple Scheduler implementation

    Runs tasks after a set amount of time"""

    def __init__(self, delay_in_s: float, bot: Bot):
        self.delay = delay_in_s
        self.bot = bot

    async def run_forever(self, task: Task) -> None:
        await self.bot.wait_until_ready()
        await self.bot.wait_until_guild_available()
        is_coro = iscoroutinefunction(task.run)

        try:
            if iscoroutinefunction(task.run_once):
                await task.run_once()
            else:
                task.run_once()  # type: ignore

            while not self.bot.is_closed():
                if is_coro:
                    await task.run()
                else:
                    task.run()  # type: ignore

                await sleep(self.delay)
        except Exception as exception:
            log.exception(exception)
            raise exception
