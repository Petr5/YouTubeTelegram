import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Папка для скачанных видео
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Конфигурация yt_dlp для mp4
YDL_OPTIONS = {
    'format': 'mp4',
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
}


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Пришли ссылку на YouTube-видео или Shorts — я скачаю и пришлю тебе .mp4.")


@dp.message()
async def download_video(message: types.Message):
    url = message.text.strip()

    if not url.startswith("http"):
        return await message.reply("Пожалуйста, отправь корректную ссылку на YouTube.")

    await message.reply("⏬ Скачиваю видео, подожди немного...")

    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
    except Exception as e:
        return await message.reply(f"⚠️ Ошибка при загрузке: {e}")

    if os.path.exists(filename):
        video = FSInputFile(filename)
        await message.reply_video(video)
        os.remove(filename)
    else:
        await message.reply("❌ Не удалось найти видеофайл после загрузки.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
