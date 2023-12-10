#pip install git+https://github.com/openai/whisper.git
#Установка whisper

import spacy
from spacy.lang.ru import Russian
from spacy.lang.ru.stop_words import STOP_WORDS
import ru_core_news_sm
from string import punctuation
from heapq import nlargest

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
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    #Вычисление относительнйо частоты слов
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency

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

if __name__ == '__main__':
    result = create_transcription('/workspaces/Tg_bot/ffmpeg/voice_file/file_43.oga')
    print(summarize(result['text'], 0.5))
