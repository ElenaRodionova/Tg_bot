from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import logging

# Инициализация бота
updater = Updater(token='6637006109:AAGTrsKc4vipd6e8ZhGwBXRBoe54pjL7DnE', use_context=True)
dispatcher = updater.dispatcher

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я ТГ-бот. отправь мне свой вопрос и я дам ответ.")

# Обработчик текстовых сообщений
def echo(update, context):
    text = update.message.text

    # Здесь вы можете использовать предобученную модель для обработки текста и получения ответа

    response = "Твой текст: " + text  # Заглушка для ответа, пока предобученная модель не добавлена

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Команды и сообщения для обработки
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

# Запуск бота
updater.start_polling()
