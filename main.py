import telebot
botTimeWeb = telebot.TeleBot('6637006109:AAGTrsKc4vipd6e8ZhGwBXRBoe54pjL7DnE')
from telebot import types
import tensorflow as tf
import numpy as np
import re
from nltk.tokenize import word_tokenize

@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
  first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!"
  botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html')
botTimeWeb.infinity_polling()

model = tf.keras.models.load_model('saved_lstm_model.h5')

@botTimeWeb.message_handler(func=lambda message: True)
def reply_message(message):
    
    text = message.text

    input_data = preprocess(text)
    
    output_data = model.predict(input_data)
 
    reply_text = postprocess(output_data)
    
    botTimeWeb.reply_to(message, reply_text)

botTimeWeb.polling()


def preprocess(text):
  text = re.sub("[^a-zA-Z]"," ",text)
  text = text.lower()
  tokens = [word.strip() for word in word_tokenize(text)]
  return tokens
   
def postprocess(output_data):
  tokens = []
  for prediction in output_data:
      token = np.argmax(prediction)
      tokens.append(token)

  reply_text = " ".join(tokens)

  return reply_text
  