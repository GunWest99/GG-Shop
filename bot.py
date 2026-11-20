import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ТВОИ ДАННЫЕ (ВСТАВЬ СЮДА ТОКЕНЫ ИЗ ШАГА 1)
BOT_TOKEN = "9051099359:AAHjU_efp7ko6QprQLZus5zIomF1P7HUZfk"
ADMIN_ID = 8783227095  # Твой ID цифрами
BS_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdhOTMwYjcwLTVjNDktNDVkNS04OGI0LTc5NmJmZjFlNTYwMSIsImlhdCI6MTc5NTE4NDA3NSwic3ViIjoiZGV2ZWxvcGVyLzIzNDllZGE0LWIwYzktNDIxN S1hZWY5LTRkYTM3NmEzMmRiMSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lk cnMiOlsiMTI4LjEyOC4xMjguMTI4Il0sInR5cGUiOiJjbGllbnQifV19._53zhp6cs5jq__ Bms3tVFtBXfwIxA70DNpQN1IslH4WxsZpeVLpNWKVJ-1_3_O_tt4olUqqo9U9_ETHfObStaw"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Простая имитация базы данных (пока без сервера)
# В будущем мы заменим это на SQLite
emails_db = []

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "👋 Привет, Админ!\n\n"
        "Я бот для скупки аккаунтов Brawl Stars.\n"
        "Доступные команды:\n"
        "➕ /add email@mail.ru — добавить почту\n"
        "🗑 /delete email@mail.ru — удалить почту\n"
        "📋 /list — список свободных почт\n"
        "📩 /code 123456 — отправить код продавцу"
    )

@dp.message_handler(commands=['add'])
async def add_email(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Используй: /add email@mail.ru")
        return
    
    email = args[1].strip()
    if email in emails_db:
        await message.answer(f"⚠️ Почта {email} уже есть в базе.")
        return
    
    emails_db.append(email)
    await message.answer(f"✅ Почта {email} добавлена в пул свободных.")

@dp.message_handler(commands=['delete'])
async def delete_email(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Используй: /delete email@mail.ru")
        return
    
    email = args[1].strip()
    if email not in emails_db:
        await message.answer(f"⚠️ Почты {email} нет в базе.")
        return
    
    emails_db.remove(email)
    await message.answer(f"🗑 Почта {email} удалена из пула.")

@dp.message_handler(commands=['list'])
async def list_emails(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав.")
        return
    
    if not emails_db:
        await message.answer("📭 Свободных почт нет.")
        return
    
    text = "📋 **Свободные почты:**\n\n"
    for i, email in enumerate(emails_db, 1):
        text += f"{i}. {email}\n"
    
    await message.answer(text, parse_mode="Markdown")

@dp.message_handler(commands=['code'])
async def send_code(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет прав.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Используй: /code 123456")
        return
    
    code = args[1].strip()
    # Пока просто выводим код в чат. Позже мы отправим его на сайт.
    await message.answer(f"📩 Код `{code}` принят. В будущем он улетит на сайт продавцу.", parse_mode="Markdown")

if __name__ == '__main__':
    print("Бот запущен...")
    executor.start_polling(dp, skip_updates=True)
