import telebot
from telebot import types
import os
import random
import tensorflow as tf
import numpy as np


TOKEN = '6637006109:AAGTrsKc4vipd6e8ZhGwBXRBoe54pjL7DnE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def startBot(message):
  first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет! Отправьте мне голосовое сообщение."
  bot.send_message(message.chat.id, first_mess, parse_mode='html')

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    # Получаем файл голосового сообщения
    voice = message.voice.file_id
    
    # Загружаем файл голосового сообщения
    voice_info = bot.get_file(voice)
    voice_path = voice_info.file_path

    # Обрабатываем голосовое сообщение
    # Распознать с помощью специализированных библиотек

    # Отправляем ответное сообщение
    bot.send_message(message.chat.id, 'Голосовое сообщение получено')


@bot.message_handler(commands=['help'])
def get_commands(message):
    commands_list = []
    for handler in bot.handlers:
        if handler.command:
            commands_list.append(f"/{handler.command}")
    
    commands_text = "n".join(commands_list)
    bot.reply_to(message, f"Доступные команды:n{commands_text}")
    
@bot.message_handler(commands=['clear_history'])
def clear_history(message):
    # Очистить историю запросов
    bot.clear_update_queue()
    bot.reply_to(message, "История запросов очищена.")

bot.infinity_polling()
