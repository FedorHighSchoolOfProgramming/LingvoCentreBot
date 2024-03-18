import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import datetime

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = Bot(token='6899127577:AAGFhyWUASygoqxVQSjavpamFwVLUNSpuVc')
dp = Dispatcher(bot)
chat_ids = set()

async def on_startup(dp):
    with open('chat_id.txt', 'r') as f:
        for line in f:
            chat_ids.add(int(line.strip()))

async def start(message: types.Message):
    chat_id = message.chat.id
    chat_ids.add(chat_id)
    with open('chat_id.txt', 'a') as f:
        f.write(str(chat_id) + '\n')
    await message.answer('Вы подписались на сообщения')

async def send_message():
    while True:
        now = datetime.datetime.now()
        if now.weekday() == 4 and now.hour == 18 and now.minute == 0:  # Пятница, 18:00 по московскому времени
            for chat_id in chat_ids:
                try:
                    await bot.send_message(chat_id, 'Я играю в доту', parse_mode=ParseMode.HTML)
                except Exception as e:
                    print(f'Ошибка при отправке сообщения: {e}')
        await asyncio.sleep(60)  # Проверка каждую минуту

if __name__ == '__main__':
    dp.register_message_handler(start, commands=['start'])
    loop = asyncio.get_event_loop()
    loop.create_task(send_message())
    executor.start_polling(dp, on_startup=on_startup)

