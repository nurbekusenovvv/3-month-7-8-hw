from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import config
import sqlite3
import logging
import datetime

bot = Bot(config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)


start_connect = sqlite3.connect('dodo.db')
cur  = start_connect.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS real(
    name VARCHAR(22),
    surname VARCHAR(22),
    number INTEGER(33),
    addres VARCHAR(33),
    food VARCHAR(44)
    
    )""")
start_connect.commit()


    
@dp.message_handler(commands=["start"])
async def start(message : types.Message):

    # try:
        cur  = start_connect.cursor()
        # cur.execute(f"SELECT name FROM real WHERE  name  == {message.from_user.first_name};")
        # result = cur.fetchall()
        # if result ==[]:
        #     cur.execute(f"INSERT INTO real (name,surname)VALUES ('{message.from_user.first_name}',  '{message.from_user.last_name};")
        #     start_connect.commit()
      
        
        inline_1 = InlineKeyboardButton("номер",callback_data="contact")
        inline_2 = InlineKeyboardButton("адрес",callback_data="location")
        inline_3 = InlineKeyboardButton("заказ еда",callback_data="food")
    

        inline_kb = InlineKeyboardMarkup().add(inline_1,inline_2,inline_3)
        await message.answer(f"Ас саламу алейкум ,{message.from_user.full_name}. Вас приветствует администрация DODO PIZZA.\n"
                "Если хотите заказать еду нажмите кнопку",reply_markup=inline_kb)            
    # except:
    #     await message.answer("Вышли не большие ошибки обратитесь тех.админу: ")
    

@dp.callback_query_handler(lambda callbak: callbak.data == 'contact')
async def process_callback_button1(callbak: types.CallbackQuery):
    kb = [
        [KeyboardButton("/contact", request_contact=True)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await callbak.message.answer(f"Нажата_кнопка_контакта!", reply_markup=keyboard)

    

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(msg:types.Message):
    
        await msg.reply("OK")
        num = cur.execute(f"UPDATE real SET number = {msg.contact['phone_number']} WHERE ('{msg}')")
        start_connect = start_connect.execute(f"INSERT INTO real (number) VALUES ('{num}');")
    
        start_connect.commit()
        # await state.finish() 

@dp.callback_query_handler(lambda callbak: callbak.data == 'location')
async def process_callback_button1(callbak: types.CallbackQuery):
    kb = [
        [KeyboardButton("/location", request_location=True)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await callbak.message.answer(f"Нажата_кнопка_локации!", reply_markup = keyboard)

@dp.message_handler(content_types=types.ContentType.LOCATION) 
async def get_location(msg:types.Message):
    
    cur.execute(f"INSERT INTO real (id_user, address_longitude, address_latitude) VALUES ({msg.from_user.id}, {msg.location['latitude']}, {msg.location['longitude']})")
    start_connect.commit()
    await msg.reply("OK")
    
@dp.callback_query_handler(lambda callbak: callbak.data == 'food')
async def process_callback_button1(callbak: types.CallbackQuery):
    kb = [
        [KeyboardButton("Заказать еду!")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    await callbak.message.answer(f"Нажата_кнопка_Заказать еду!", reply_markup = keyboard)

class ContactForm(StatesGroup):
    client = State()

@dp.message_handler(text = 'Заказать еду!')
async def start(message : types.Message):
    await message.answer("Введите ваш заказ: ")
    await ContactForm.client.set()



@dp.message_handler(state=ContactForm.client)
async def get_contact(message: types.Message, state: FSMContext):
    # try:
    # times = datetime.datetime.now()
        
    cur_contact = start_connect.cursor()
    # res = message.text.replace(",","",).split()
    order = message.text
    cur_contact = cur_contact.execute(f"INSERT INTO real (food) VALUES ('{order}');")
    start_connect.commit()
    await state.finish()    
    # except:

        
executor.start_polling(dp)
