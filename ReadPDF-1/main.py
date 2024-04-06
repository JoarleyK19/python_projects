import os
import PyPDF2
import pyttsx3
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.data.path.append("C:\\Users\\Joarley Kelix\\AppData\\Roaming\\nltk_data")
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


def extract_text_pdf(file):
    text = ""
    dirlist = os.listdir("./")
    for i in dirlist:
        filename = os.path.join("/")
        full_path = os.path.abspath(filename + i)
        if file in full_path:
            with open(file, 'rb') as arquivo:
                leitor_pdf = PyPDF2.PdfReader(arquivo)
                num_paginas = len(leitor_pdf.pages)
                for pagina in range(num_paginas):
                    text += leitor_pdf.pages[pagina].extract_text()
    return text


def clean_text_pdf(text):
    # Remover caracteres especiais e espaços em branco extras
    clean_text = re.sub(r'[^a-zA-Z0-9\n]', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text


def text_to_audio(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('portuguese'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    clean_text = ' '.join(lemmatized_tokens)

    # Sintetizar áudio
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(clean_text)
    engine.runAndWait()


# Extrair texto do PDF
extract_text = extract_text_pdf("ril_v57_n225_p43.pdf")
# Limpar texto extraído
# cleaned_text = clean_text_pdf(extract_text)
# Converter texto limpo em áudio
text_to_audio(extract_text)
