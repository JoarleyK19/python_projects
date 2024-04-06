import os

import PyPDF2
import pyttsx3
import re

import requests


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


def clean_text_pdf(file):
    clean_text = re.sub(r'[^a-zA-Z0-9\n]', '', file)
    return clean_text


def test_text():
    text = """
        A Inteligência Artificial está se espalhando rapidamente em nossa vida cotidiana e o mundo do trabalho não é exceção.
        Inteligência artificialA IA está cada vez mais a moldar o contexto do emprego: essas áreas emergentes são a tomada de decisões
        Tomada de decisão automatizadaaumentada e automatizada. Como a tomada de decisões baseada em IA é alimentada por dados pessoais, a
        Proteção de dadosconformidade com os quadros de proteção de dados é inevitável.
    """
    return text


def test_connect_pipenv():
    response = requests.get('https://httpbin.org/ip')

    print('Your IP is {0}'.format(response.json()['origin']))


def text_to_audio(text):
    clean_text = clean_text_pdf(text)
    motor = pyttsx3.init()
    motor.setProperty('rate', 150)
    motor.setProperty('volume', 2.0)
    motor.setProperty('voice', 'brazil')
    motor.say(clean_text)
    motor.runAndWait()


# extract_text = extract_text_pdf("artigo.pdf")
text_to_audio(test_text())

# test_connect_pipenv()
