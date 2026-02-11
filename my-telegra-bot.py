import os
import random
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Загружаем треки - БЕЗ УСЛОВИЙ!
tracks = []
file_path = 'handle track list.txt'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Берем любые непустые строки, игнорируем только комментарии и файлы
            if line and not line.startswith('[') and not line.startswith('Output'):
                tracks.append(line)
    print(f"Загружено треков: {len(tracks)}")
except Exception as e:
    print(f"Ошибка: {e}")

# Если все еще пусто - используем запасные треки
if not tracks:
    tracks = [
        "человек-кресло",
        "человек-лужа",
        "человек-жаба",
        "женщина-кошка",
        "гном-пидор",
        "ковёр-кровать",
        "кресло-холодильник",
        "микроволновка-телевизор",
        "медиатор-гитара"
    ]
    print(f"Использую запасные треки: {len(tracks)}")

# Слова для генерации
words = []
for track in tracks:
    # Разбиваем по дефису или пробелу
    parts = track.replace('-', ' ').replace('—', ' ').replace('–', ' ').split()
    words.extend(parts)

unique_words = list(set(words)) if words else ['кресло', 'лужа', 'жаба', 'кошка', 'гном', 'зубы', 'рис']

artists = ['человек', 'гном', 'кот', 'робот', 'Егор', 'дед', 'сосед', 'алкоголик']
templates = ['{word1}-{word2}', '{artist}-{word1}', '{word1} {word2}', 'про {word1} и {word2}']


def generate_title():
    w1 = random.choice(unique_words)
    w2 = random.choice(unique_words)
    artist = random.choice(artists)
    template = random.choice(templates)

    return template.format(artist=artist, word1=w1, word2=w2)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Это генератор названий треков\n"

        "/random — реальный трек\n"
        "/go — сгенерировать"
    )


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    track = random.choice(tracks)
    await message.answer(f"{track}")


@dp.message(Command("go"))
async def cmd_go(message: types.Message):
    title = generate_title()
    await message.answer(f"{title}")


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())