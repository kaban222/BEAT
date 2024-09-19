import datetime
import random
from datetime import timedelta
from datetime import datetime
from operator import itemgetter

from aiogram import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json

from flask import Flask, render_template, request
from threading import Thread

import projectSettings

if projectSettings.host:
    PROXY_URL = "http://proxy.server:3128"
    bot = Bot(projectSettings.tok, parse_mode="HTML", disable_web_page_preview=True, proxy=PROXY_URL)
    dp = Dispatcher(bot)
else:
    bot = Bot(projectSettings.tok, parse_mode="HTML", disable_web_page_preview=True)
    dp = Dispatcher(bot)

app = Flask('app')

chanel_link = "https://t.me/Gbb_dev"
chat_link = "https://t.me/Gbb_talks"

music = projectSettings.misic

#///////////////////      BD
BD = {}
Band = {}


def load():
    global BD, Band
    try:
        f1 = open("BD/Persons.json", "r")
        BD = json.load(f1)
        f1.close()
    except:
        print("Ошибка загрузки Файла #1 \nBD/Persons.json")

    try:
        f1 = open("BD/Bands.json", "r")
        Band = json.load(f1)
        f1.close()
    except:
        print("Ошибка загрузки Файла #2 \nBD/Bands.json")

def save():
    global BD
    f1 = open("BD/Persons.json", "w")
    json.dump(BD, f1, ensure_ascii=False)
    f1.close()

def save_band():
    global Band
    f1 = open("BD/Bands.json", "w")
    json.dump(Band, f1, ensure_ascii=False)
    f1.close()

async def registration(kkk):
    global BD
    if kkk not in BD.keys():
        BD[kkk] = {
            "note": 100,
            "balance": 0,
            "admin": False,
            "band": "00",
            "name": "Игрок",
        }
        save()
        print(f"Новая регистрация {datetime.now()} \nid:{kkk}")



async def send_balance(msg, kkk):
    mention = "<a href='tg://openmessage?user_id=" + kkk + "'>" + BD[kkk]['name'] + "</>"
    txt = f"{mention}, ваш баланс: \n" \
          f"\n" \
          f"        ⌈🎶Ноты  ⧽  {BD[kkk]['note']}⌋\n" \
          f"        ⌈⭐Звёзды  ⧽  {BD[kkk]['balance']}⌋\n" \
          f"\n" \
          f"❓Нужна помощь — /help"

    await bot.send_photo(msg.chat.id, open("assets/bank1.jpeg", "rb"), caption=txt)

async def play_instrument(msg, kkk):
    mention = "<a href='tg://openmessage?user_id=" + kkk + "'>" + BD[kkk]['name'] + "</>"

    goer = False
    if "timer_1" not in BD[kkk].keys():
        goer = True
        BD[kkk]['timer_1'] = str(msg.date)
    else:
        date_last_farm = datetime.strptime(str(BD[kkk]["timer_1"]), "%Y-%m-%d %H:%M:%S")
        date2 = datetime.strptime(str(msg.date), "%Y-%m-%d %H:%M:%S")
        tm = date2 - date_last_farm
        tm2 = int(tm.total_seconds())
        if tm2 >= 7200:
            goer = True
            BD[kkk]['timer_1'] = str(msg.date)
        else:
            goer = False
            await bot.send_message(msg.chat.id, f"{mention}, Играть на гитаре можно раз в два часа! Приходи позже")

    if goer:
        rand = random.randint(50, 150)
        await bot.send_message(msg.chat.id, f"{mention}, Вы сыграли на гитаре! Ваши достижения: {rand} нот")
        BD[kkk]['note'] += rand
        save()

async def all_bands(msg, kkk):
    mention = "<a href='tg://openmessage?user_id=" + kkk + "'>" + BD[kkk]['name'] + "</>"
    D_list = {}
    for i, y in Band["all"].items():
        D_list[i] = y['gold']

    sorted_tuple = dict(sorted(D_list.items(), key=itemgetter(1)))
    lst = []
    kol = 0
    for _i in sorted_tuple.keys():
        lst.append(_i)
        kol += 1
    sorted_tuple = {}
    lenth = kol
    for i in range(lenth):
        lenth -= 1
        sorted_tuple[lst[lenth]] = str(Band['all'][lst[lenth]]['gold'])

    kol = 1
    txt = f"{mention}, топ группы по коронам:\n" \
          f"\n"
    for i, y in sorted_tuple.items():
        txt += f"{kol}. <b>[{Band['all'][i]['name']}]</b> - {projectSettings.money_form(str(y))}👑\n"
        kol += 1
        if kol >= 10:
            break

    await bot.send_message(msg.chat.id, txt)

async def form_txt(txt):
    txt = str(txt)
    ready = ""
    for i in txt:
        if i not in [" "]:
            ready += i
    return str(ready.lower())

def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None

@dp.message_handler(commands=["band", "Band"], state="*")
async def start_command(msg: types.Message):
    kkk = str(msg.from_user.id)
    if BD[kkk]['band'] == "00":
        await bot.send_message(msg.chat.id, "Вы не состоите не в одной группе!")
    else:
        await bot.send_message(msg.chat.id, "скоро добавим!")

@dp.message_handler(commands=["help", "Help"], state="*")
async def start_command(msg: types.Message):
    kkk = str(msg.from_user.id)
    await registration(kkk)
    b_start = InlineKeyboardMarkup()
    b_start.add(InlineKeyboardButton("💬Канал || Новости", url=chanel_link))
    await bot.send_message(msg.chat.id, "Скоро обновим список!", reply_markup=b_start)

@dp.message_handler(commands=["start", "Start"], state="*")
async def start_command(msg: types.Message):
    kkk = str(msg.from_user.id)
    unique_code = str(extract_unique_code(msg.text))
    await registration(kkk)
    CMD = False
    work = False
    if unique_code in BD.keys():
        CMD = True
    if str(unique_code).split("_")[0] == "w":
        work = True
    b_start = InlineKeyboardMarkup()
    b_start.add(InlineKeyboardButton("💬Чат", url=chat_link))
    b_start.add(InlineKeyboardButton("💬Канал", url=chanel_link))
    mention = "<a href='tg://openmessage?user_id=" + kkk + "'>" + BD[kkk]['name'] + "</>"
    txt = f"{mention}, Добро пожаловать в Beat bot! \n" \
          f"\n" \
          f"Мы поддерживаем любые направления музыки, и даём полную свободу в игре!\n" \
          f"\n" \
          f"Мы надеемся вы найдёте своё место, удачи!"

    await bot.send_message(msg.chat.id, txt, reply_markup=b_start)

make_group = {}
@dp.message_handler()
async def sistema(msg: types.Message):
    global BD
    kkk = str(msg.from_user.id)
    await registration(kkk)
    txt = await form_txt(msg.text)

    mention = "<a href='tg://openmessage?user_id=" + kkk + "'>" + BD[kkk]['name'] + "</>"

    if txt in ["б", "баланс"]:
        await send_balance(msg, kkk)

    if txt in ["играть"]:
        await play_instrument(msg, kkk)

    if txt in ["группы", "групы", "банды", "музыканты"]:
        await all_bands(msg, kkk)



    if kkk in make_group.keys():
        if str(msg.chat.id) == make_group[kkk]:
            if len(msg.text) > 16 or len(msg.text) < 1:
                await bot.send_message(msg.chat.id, "имя должно быть от 1 доо 16 символов!")
            elif BD[kkk]['note'] < 1000:
                await bot.send_message(msg.chat.id, f"Вам нехвтило манет! Осталось накопить: {1000 - BD[kkk]['note']}")
            else:
                if BD[kkk]['band'] != "00":
                    await bot.send_message(msg.chat.id, "cначала нужно выйти из прошлой группы")
                else:
                    Band['all'][str(Band['kol'])] = {"name": str(msg.text), "owner": kkk, "peoples": [{"id": kkk, "status": 5}], "note": 0, "gold": 1}
                    BD[kkk]['band'] = str(Band['kol'])
                    BD[kkk]['note'] -= 1000
                    Band['kol'] += 1
                    save()
                    save_band()
                    await bot.send_message(msg.chat.id, f"Вы создали группу под названием {msg.text}. \n\nУправление группой - /band")

    if txt in ["создатьгруппу"]:
        await bot.send_message(msg.chat.id, f"{mention}, Чтобы создать группу:\n1.Стоимость 1000 Нот \n\nЕсли все условия соблюдены, напишите имя для вашей группы до 16 символов.")
        make_group[kkk] = str(msg.chat.id)

def run():
    app.run()

@app.route('/')
def index_page():
    return f"Спасибо, что играете!"

if __name__ == "__main__":
    load()
    print(f"[{str(datetime.now()).split('.')[0]}]Бот работает! \nЗарегестрированых: {len(BD)}")
    server = Thread(target=run)
    server.start()
    executor.start_polling(dp)

