from ast import BinOp
from datetime import datetime
from dis import Bytecode
from operator import xor
from random import randint
from datetime import datetime, timedelta
from sched import scheduler
from aiogram.dispatcher import FSMContext
from string import printable
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types

from database_class import Database
from wordlist import wordlist

printable = printable[0:-9]
printable.replace(" ", '')

MIN = 0
MAX = len(printable) - 1
API_TOKEN = '545'


bot = Bot(token='545')
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    check = db.insert_user(message["from"]["id"], message["from"]["first_name"])
    start_message = f"""
Привет, *{message["from"]["username"]}* 😀
Этот бот тебе поможет создать реально *БЕЗОПАСНЫЕ* пароли and парольные фразы длиной от 4 до 256 и от 4 до 100 соответственно 🔐
Нажми на команду */help* для просмотра возможностей, либо взгляни на "меню"
"""

    await message.reply(start_message, parse_mode="Markdown")


@dp.message_handler(commands=['help'])
async def echo(message: types.Message):

    db.insert_user(message["from"]["id"], message["from"]["first_name"])

    help_message = f"""
*/start* - начальное сообщение
*/gen* - создать пароль длиной в 32 символа
*/gen num* - для создания пароля длиной в число символов
*/gen 8*
*/gen 10*
*/gen 16*
*/gen 64*
🔑 Пароли сгенерированные с помощью команды /gen очень надёжны, 
💪 Но их сложно запомнить. У вас должно быть немного мужества, чтобы запомнить его.
Если вы хотите запомнить этот пароль, но более лёгким способом - используйте парольную фразу. Парольная фраза - это своего рода пароль, представляющий собой комбинацию нескольких `n` разных слов, как показано ниже.
Парольная фраза: _absentee afternoon plus repackage long_
/phrase - для генерации парольной фразы длиной 8 слов
/phrase num - создайте парольную фразу из num слов
Пример: 
*/phrase 4*
*/phrase 8*
*/phrase 12*
*/phrase 20*

*МАЛЕНЬКИЕ ОСОБЕННОСТИ:*
----------------------
*/save* - сохранить любые заметки или пароли
Примечание: все сохранённые заметки зашифрованы, и никто без действительного ключа расшифровки не сможет прочитать заметки.
example:
/save _Мне нужно встретиться с другом сегодня в 12:30!_
/save _Мой пропуск в клуб: DeDiNsIdE228_
---------------------
*/get* - сохранить или получить все сохранённые заметки

*ДРУГИЕ КОМАНДЫ:*
*/stat* - посмотреть свою статистику
*/gstat* - посмотреть глобальную статистику
*/dev* - посмотреть информацию о разрабе
    """

    await message.reply(help_message, parse_mode="Markdown")


@dp.message_handler(commands=['gen'])
async def gen(message: types.Message):

    length = message.text.replace("/gen", '').strip()

    try:
        if len(length) == 0:
            length = 16
        else:
            length = int(length)

        if 4 <= length <= 256:

            passwords = ""
            for _ in range(5):
                passwords += "\n\n" + (generate(length))

            db.increase_password_count(message["from"]["id"], 5)
            msg = f"""🔐 Ваши сгенерированные пароли:
                {passwords[1:]}
                """
            await message.reply(msg)
        elif length <= 3:
                await message.reply("Слишком маленький... 🤏")
        elif length > 256:
                await message.reply("Слишком длинный... 🤥")
    except:
        await message.reply("🔢 Пожалуйста введите номер!")


@dp.message_handler(commands=['phrase'])
async def phrase(message: types.Message):

    length = message.text.replace('/phrase', '').strip().replace(" ", '')

    try:
        if len(length) == 0:
            length = 8
        
        try:

            if length != 8:
    
                length = int(length)
            if 4 <= length <= 100:

                phrases = ""

                for _ in range(5):
                    phrase = ""
                    for _ in range(length):

                        phrase += " " + wordlist[randint(0,len(wordlist)-1)]

                    phrases += "\n\n" + phrase
                msg = f"""👍 Кодовые фразы сгенерированны:
                    {phrases[1:]}
                    """
                db.increase_passphrase_count(message["from"]["id"], 5)
                await message.reply(msg)

            elif length <= 3:
                await message.reply("Слишком маленький... 🤏")

            elif length > 100:
                await message.reply("Сликшом длинный... 🤥")
    
        except:
            await message.reply("🔢 Пожалуйста введите номер!")
    
    except Exception as e:
        await message.reply("📔 Пожалуйста, укажите действительную команду")


@dp.message_handler(commands=['stats', 'stat', 'statistics'])
async def user_stat(message):

    stats = db.user_stat(message["from"]["id"])
    passwords_generated = stats[0]
    passphrases_generated = stats[1]
    msg = f"Ты сгенерировал *{passwords_generated}* надёжных паролей 🔐 и *{passphrases_generated}* 🔐 лёгких кодовых фраз"
    
    del stats
    del passphrases_generated
    del passwords_generated

    await message.reply(msg, parse_mode="Markdown")


@dp.message_handler(commands=['gstats', 'gstat', 'gstatistics'])
async def global_stat(message):

    stats = db.global_stat()
    passwords_generated = stats[0]
    passphrases_generated = stats[1]

    msg = f"Пользователи сгенерировали *{passwords_generated}* надёжных паролей 🔐 и *{passphrases_generated}* 🔐 лёгких кодовых фраз"
    
    del stats
    del passphrases_generated
    del passwords_generated
    
    await message.reply(msg, parse_mode="Markdown")


@dp.message_handler(commands=['dev', 'developer', 'builder'])
async def dev(message):
    
    msg = f"""Привет, *{message["from"]["first_name"]}* 😀
    Меня зовут Илья и ты можешь написать мне в *Telegram* для заказа бота/сайта/мини-приложения @likemyasspls! А также у нас есть канал (@NoLupi)
    Ты можешь посмотреть мои проекты на этом сайте: *github.com/NoLupiPls*
    """
    await message.reply(msg, parse_mode="Markdown")


@dp.message_handler(commands=['save'])
async def save_notes(message):
    msg = message["text"].replace('/save', '', 1).strip()
    if len(msg) > 0:


        db.save_notes(message["from"]["id"], msg, datetime.now().strftime("%y-%m-%d %H:%M:%S"))
        await message.reply("✅ Сохранено")
    else:
        await message.reply("Отправьте что-нибудь, чтобы сохранить 😕")


@dp.message_handler(commands=['get'])
async def get_saved_notes(message):
    
    data = db.get_notes(message["from"]["id"])

    if len(data) > 0:
        msg = '''📖 Ваши сохранённые заметки:'''
        for i in data:
            msg += "\n\n" + enc.decrypt_data(i[0])
        await message.reply(msg)
        del enc
    else:
        await message.reply("Вы ещё не сохранили ни одной заметки 😕")




class Wait(StatesGroup):
    lol = State()

@dp.message_handler(commands=['bin'], state='*')
async def bin(message: types.Message):
    await message.answer("Введите пароль, который вы хотите перевести в двоичный код")
    await Wait.lol.set()
    
@dp.message_handler(state = Wait.lol)
async def pip_lol(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = str(data['text'])
    state.finish
    if len(message.text) > 124:
        await message.answer("❌ Извините, больше 124 символов - нельзя")
        return
    
    '''
    await message.reply("☑ Подождите пожалуйста, идёт перекодировка...")
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = str(data['text'])
    '''
    
    res = ''.join(format(ord(i), ' b') for i in user_message)
    #key = b'key'
    #xor(user_message.encode(), key)
    
    bad = res
    await message.answer('Вот твой код:\n' + bad)
    
        
    executor.return_polling(dp)
        
        
@dp.message_handler()
async def same_reply(message):
    db.insert_user(message["from"]["id"], message["from"]["first_name"])
    await message.reply(f"Хэй, {message['from']['username']}, я не знаю о чём ты говоришь😅")


def generate(length):
    password = ""
    for _ in range(length):
        password += printable[randint(MIN, MAX)]
    return password
    
        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
