import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model  # type: ignore

lemmatizer_gbot = WordNetLemmatizer()

# Cargar los datos de intenciones
intenciones_gbot = json.loads(open('intenciones_gbot_esp.json', 'r', encoding='utf-8').read())
palabras_gbot = pickle.load(open('palabras_gbot.pkl', 'rb'))
clases_gbot = pickle.load(open('clases_gbot.pkl', 'rb'))
modelo_gbot = load_model('modelo_chatbot_gbot.h5')

def limpiar_frase_gbot(frase_gbot):
    palabras_frase_gbot = nltk.word_tokenize(frase_gbot)
    palabras_frase_gbot = [lemmatizer_gbot.lemmatize(word.lower()) for word in palabras_frase_gbot]
    return palabras_frase_gbot

def bolsa_de_palabras_gbot(frase_gbot):
    palabras_frase_gbot = limpiar_frase_gbot(frase_gbot)
    bolsa_gbot = [0]*len(palabras_gbot)
    for palabra_gbot in palabras_frase_gbot:
        for i, palabra_gbot_en_lista in enumerate(palabras_gbot):
            if palabra_gbot_en_lista == palabra_gbot:
                bolsa_gbot[i] = 1
    return np.array(bolsa_gbot)

def predecir_clase_gbot(frase_gbot):
    bolsa_gbot = bolsa_de_palabras_gbot(frase_gbot)
    res_gbot = modelo_gbot.predict(np.array([bolsa_gbot]))[0]
    UMBRAL_ERROR_GBOT = 0.25
    resultados_gbot = [[i, r] for i, r in enumerate(res_gbot) if r > UMBRAL_ERROR_GBOT]
    resultados_gbot.sort(key=lambda x: x[1], reverse=True)
    lista_retorno_gbot = []
    for r in resultados_gbot:
        lista_retorno_gbot.append({'intencion': clases_gbot[r[0]], 'probabilidad': str(r[1])})
    return lista_retorno_gbot

def obtener_respuesta_gbot(lista_intenciones_gbot, json_intenciones_gbot):
    etiqueta_gbot = lista_intenciones_gbot[0]['intencion']
    lista_de_intenciones_gbot = json_intenciones_gbot['intenciones']
    for i in lista_de_intenciones_gbot:
        if i['etiqueta'] == etiqueta_gbot:
            resultado_gbot = random.choice(i['respuestas'])
            break
    return resultado_gbot
