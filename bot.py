import asyncio
import logging
from http.client import responses

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from openai import OpenAI

TOKEN = ''
logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

a = {}
e = [
    {"n": "германтин мяч",     "p": 2000, "q": 5},
    {"n": "яблоко",  "p": 100,  "q": 45},
    {"n": "хлеб",    "p": 150,  "q": 20},
    {"n": "ламбада",  "p": 200,  "q": 30},
    {"n": "капилка",     "p": 800,  "q": 10},
    {"n": "банан",   "p": 120,  "q": 25},
    {"n": "картошка","p": 80,   "q": 50},
    {"n": "курица",  "p": 600,  "q": 15},
    {"n": "рис",     "p": 250,  "q": 40},
    {"n": "яйцо",    "p": 20,   "q": 100},
    {"n": "Кока-кола", "p" : 500, "q": 21}
]
g = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я — Наурызбай, владелец магазина. Если есть вопросы — просто напиши 🙂', parse_mode="HTML")

@dp.message(lambda message: message.text or message.photo or message.document)
async def filter_messages(message: Message):
    c = message.chat.id

    if c in g and g[c]:
        g[c] = False
        await message.answer("Спасибо! Платёж получил. Благодарю за покупку!", parse_mode="Markdown")
        return

    if message.text and 'оплат' in message.text.lower():
        await message.answer("Для оплаты отправьте деньги на Kaspi: 8 707 298 06 63 и пришлите чек.")
        g[c] = True
        return

    if not message.text:
        return

    if c not in a:
        a[c] = []
    a[c].append({"role": "user", "content": message.text})
    a[c] = a[c][-10:]

    f = "Меня зовут Наурызбай, я владелец магазина под названием «Қарама-қарсы». Ниже приведён список товаров, представленных в магазине.:\n"
    for i in e:
        f = f + i["n"] + " — " + str(i["p"]) + " тг — " + str(i["q"]) + "\n"
    b = [{"role": "system", "content": f + "\nТы — продавец в небольшом магазине. Отвечай как живой человек: дружелюбно, вежливо, с желанием помочь. Всегда старайся быть полезным. Если уместно — поприветствуй, попрощайся, поблагодари. Отвечай на том языке, на котором с тобой разговаривают. Не пиши слишком формально — говори просто и по-доброму."}] + a[c]

    client = OpenAI(
        base_url="https://api.langdock.com/openai/eu/v1",
        api_key="sk-p0N53JZL_hWs4LGqmSBa1mIoJLGJfzOUdTu6UdSSrQCs_K6sVntjg82xbbXsm0HhJ9skFtEucO7SHu8Q6WNHeQ"
    )
    d = client.chat.completions.create(
        model="gpt-4o",
        messages=b
    ).choices[0].message.content

    a[c].append({"role": "assistant", "content": d})
    a[c] = a[c][-10:]
    await message.answer(d, parse_mode="Markdown")

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

