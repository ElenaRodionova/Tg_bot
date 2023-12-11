#pip install git+https://github.com/openai/whisper.git
#Установка whisper
#pip install https://github.com/explosion/spacy-models/releases/download/ru_core_news_sm-3.1.0/ru_core_news_sm-3.1.0.tar.gz
#Установка русского языка для spacy

import whisper
import spacy
from spacy.lang.ru import Russian
from spacy.lang.ru.stop_words import STOP_WORDS
import ru_core_news_sm
from string import punctuation
from heapq import nlargest
import os
import torch

def create_transcription(path):
    """
    Возможно создание переведенной транскрипции и её превращение в звук
    """
    #Скачивание модели. Medium весит много, можно использовать small или base
    model = whisper.load_model("base")
    result = model.transcribe(path)
    print(result["text"])
    return result

def summarize(text, per):
    """
    Summary текста. Необходимы исправления 
    """
    nlp = spacy.load('ru_core_news_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    
    #Вычисление абсолютной частоты слов
    for word in doc:
        if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
            if word.text not in word_frequencies:
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    if not doc:
        return "No text provided."
    
    #Вычисление относительнйо частоты слов
    max_frequency = max(word_frequencies.values())
    word_frequencies = {word: freq/max_frequency for word, freq in word_frequencies.items()}

    #Вычисление рейтингов предложений
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    
    #Фильтрация предложений по рейтингу и объединение результата
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)

    return summary

def translate_to_eng(path):
    """
    Перевод на английский и озвучивание
    Сохраняет аудио на компьютере
    """
    #small, base, medium
    model = whisper.load_model("small")

    result = model.transcribe(path, task="translate")

    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt', local_file)  

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    #example_text = 'oh no pizza delivery is closed, i guess ill order something from yandex lavka then. I wonder if they will search for available courier for an eternity like last time'
    sample_rate = 48000
    speaker='en_0'

    audio_paths = model.save_wav(text=result['text'],
                             speaker=speaker,
                             sample_rate=sample_rate)
    print(audio_paths)
    return f"Аудиофайл сохранен, <b>{audio_paths}</b>"

if __name__ == '__main__':
    result = create_transcription('/workspaces/Tg_bot/ffmpeg/voice_file/file_51.oga')
    print(summarize(result['text'], per = 0.5))
