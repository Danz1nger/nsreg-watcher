import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
import subprocess
import os

TOKEN = os.environ["BOT_TOKEN"]
ERROR_LOGS_PATH = "logs/grabber_errors.log"
SPIDERS_SCRIPT_PATH = "compose/scrapy/scrapy-dev.sh"
CHAT_ID = os.environ["CHAT_ID"]

router = Router()
bot = Bot(TOKEN, parse_mode="markdown")


def cut_log(log: str) -> str:
    """
    Make log shorter if len > 4000
    """
    log = log.split("---SPLIT---")[-1]
    if len(log) > 4000:
        log = f"{log[:4001]}..."
    return log


@router.message(Command(commands=["start"]))
async def command_start_handler(*args, **kwargs) -> None:

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"🕷️🕷️🕷️ Запуск спайдеров 🕷️🕷️🕷️"
    )
    try:
        subprocess.run(["sh", f"{SPIDERS_SCRIPT_PATH}"], check=True)

        with open(ERROR_LOGS_PATH) as file:
            error_log = file.read()

        error_log = cut_log(error_log)

        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"Спайдеры завершили свою работу /╲/\(╭•̀ﮧ •́╮)/\╱\ \nError logs:\n```{error_log}```"
        )
    except subprocess.CalledProcessError as error:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"/╲/\╭[ ☉ ﹏ ☉ ]╮/\╱\ \n{error}"
        )


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    await command_start_handler()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
