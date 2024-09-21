# Настройки
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import apiai, json
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

updater = Updater(token=TELEGRAM_BOT_TOKEN) # Токен API к Telegram
dispatcher = updater.dispatcher
# Обработка команд
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который расскажет обо всем.')
def textMessage(bot, update):
    request = apiai.ApiAI(OPENAI_API_KEY).text_request() # Токен API
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'MilanAttokelvin' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
# Хендлеры
start_command_handler = CommandHandler('start', start)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(drop_pending_updates=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()