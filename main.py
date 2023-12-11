import telebot
from telebot import types
import os
import random
import tensorflow as tf
import numpy as np
from model import create_transcription
from model import summarize
from model import translate_to_eng

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

    downloaded_file = bot.download_file(voice_path)
    
    # Путь для сохранения файла
    destination_folder = "/workspaces/Tg_bot/ffmpeg/voice_file"
    destination_path = f"{destination_folder}/{voice_path.split('/')[-1]}"

    # Сохранение файла в указанную папку
    with open(destination_path, 'wb') as voice_file:
        voice_file.write(downloaded_file)

      
    bot.send_message(message.chat.id, 'Голосовое сообщение получено. Что вы хотите сделать?')
    
    keyboard = types.InlineKeyboardMarkup()
    text_button = types.InlineKeyboardButton(text='Вывести текст', callback_data='display_text')
    translate_button = types.InlineKeyboardButton(text='Перевести сообщение на английский язык', callback_data='translate_english')
    keyboard.add(text_button, translate_button)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        if call.data == 'display_text':
          # Обрабатываем голосовое сообщение
          result = create_transcription(destination_path)

          # Распознать с помощью специализированных библиотек
          summary = summarize(result['text'], per = 0.5)

          # Отправляем ответное сообщение
          bot.send_message(message.chat.id, summary, parse_mode='html')
        elif call.data == 'translate_english':
          # Перевод на английский и озвучивание. Сохранение аудио на компьютере
          audio_paths = translate_to_eng(destination_path)
          # Отправляем ответное сообщение с путем, где находится аудио
          bot.send_message(message.chat.id, audio_paths, parse_mode='html')
          audio_file = open('test.wav', 'rb')  # Открываем аудиофайл в режиме чтения байтов
          bot.send_audio(message.chat.id, audio_file)
          audio_file.close()  # Обязательно закрываем файл после отправки


bot.infinity_polling()
