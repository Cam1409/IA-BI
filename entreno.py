import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential# type: ignore
from keras.layers import Dense, Dropout # type: ignore
from keras.optimizers import SGD# type: ignore

lemmatizer_gbot = WordNetLemmatizer()

# Cargar los datos de intenciones
with open('intenciones_gbot_esp.json', 'r', encoding='utf-8') as file:
    intenciones_gbot = json.load(file)

palabras_gbot = []
clases_gbot = []
documentos_gbot = []
ignorados_gbot = ['?', '!', '.', ',']

for intencion_gbot in intenciones_gbot['intenciones']:
    for patron in intencion_gbot['patrones']:
        palabras_lista_gbot = nltk.word_tokenize(patron)
        palabras_gbot.extend(palabras_lista_gbot)
        documentos_gbot.append((palabras_lista_gbot, intencion_gbot['etiqueta']))
        if intencion_gbot['etiqueta'] not in clases_gbot:
            clases_gbot.append(intencion_gbot['etiqueta'])

palabras_gbot = [lemmatizer_gbot.lemmatize(palabra.lower()) for palabra in palabras_gbot if palabra not in ignorados_gbot]
palabras_gbot = sorted(list(set(palabras_gbot)))

clases_gbot = sorted(list(set(clases_gbot)))

print(f"Palabras: {palabras_gbot}")
print(f"Clases: {clases_gbot}")

pickle.dump(palabras_gbot, open('palabras_gbot.pkl', 'wb'))
pickle.dump(clases_gbot, open('clases_gbot.pkl', 'wb'))

entrenamiento_gbot = []
salida_gbot = []

salida_vacia_gbot = [0] * len(clases_gbot)

for documento_gbot in documentos_gbot:
    bolsa_gbot = []
    palabras_patron_gbot = documento_gbot[0]
    palabras_patron_gbot = [lemmatizer_gbot.lemmatize(palabra.lower()) for palabra in palabras_patron_gbot]
    for palabra_gbot in palabras_gbot:
        bolsa_gbot.append(1) if palabra_gbot in palabras_patron_gbot else bolsa_gbot.append(0)

    fila_salida_gbot = list(salida_vacia_gbot)
    fila_salida_gbot[clases_gbot.index(documento_gbot[1])] = 1
    entrenamiento_gbot.append(bolsa_gbot)
    salida_gbot.append(fila_salida_gbot)

entrenamiento_gbot = np.array(entrenamiento_gbot)
salida_gbot = np.array(salida_gbot)

model_gbot = Sequential()
model_gbot.add(Dense(128, input_shape=(len(entrenamiento_gbot[0]),), activation='relu'))
model_gbot.add(Dropout(0.5))
model_gbot.add(Dense(64, activation='relu'))
model_gbot.add(Dropout(0.5))
model_gbot.add(Dense(len(salida_gbot[0]), activation='softmax'))

sgd_gbot = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model_gbot.compile(loss='categorical_crossentropy', optimizer=sgd_gbot, metrics=['accuracy'])

hist_gbot = model_gbot.fit(entrenamiento_gbot, salida_gbot, epochs=200, batch_size=5, verbose=1)
model_gbot.save('modelo_chatbot_gbot.h5', hist_gbot)

print("Modelo creado y guardado")
