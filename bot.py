import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

import yt_dlp
from config import BOT_TOKEN

DOWNLOAD_DIR = "downloads"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Салам брат ✋\n"
        "Как дела?\n"
        "Что качаем сегодня? 📥🔥"
    )


@dp.message()
async def download_video(message: types.Message):
    url = message.text.strip()

    if not url.startswith("http"):
        await message.answer(
            "Братан, это чё за ссылка 😅\n"
            "Я такую не узнаю, пришли нормальную 👀"
        )
        return

    await message.answer("Всё без проблем, жди брат ⏳")

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title).80s.%(ext)s",
        "format": "bestvideo[height<=1080]+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await message.answer_video(
            FSInputFile(filename),
            caption="Братан, всё готово 😎🔥"
        )

        os.remove(filename)

    except Exception as e:
        await message.answer(
            "Братан, чё-то ошибка вылезла 😕\n"
            "Попробуй другую ссылку"
        )
        print("ОШИБКА:", e)


async def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
