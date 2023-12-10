import telebot
from telebot import types
import os
import random
import tensorflow as tf
import numpy as np
from model import create_transcription
from model import summarize

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
    
    bot.send_message(message.chat.id, 'Голосовое сообщение получено')

    # Загружаем файл голосового сообщения
    voice_info = bot.get_file(voice)
    voice_path = voice_info.file_path

    downloaded_file = bot.download_file(voice_path)
    
    # Путь для сохранения файла
    destination_folder = "/workspaces/Tg_bot/ffmpeg/voice_file"
    destination_path = f"{destination_folder}/{voice_path.split('/')[-1]}"

    # Сохранение файла в указанную папку
    with open(destination_path, 'wb') as voice_file:
        voice_file.write(downloaded_file)

    # Обрабатываем голосовое сообщение
    result = create_transcription(destination_path)

    # Распознать с помощью специализированных библиотек
    summary = summarize(summarize(result['text'], 0.5))

    # Отправляем ответное сообщение
    bot.send_message(message.chat.id, summary, parse_mode='html')

bot.infinity_polling()
