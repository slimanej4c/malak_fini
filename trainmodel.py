#IMPORT
from tkinter import *
import pandas as pd
from tensorflow import keras
from sklearn.utils import shuffle
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing import text
from sklearn.preprocessing import LabelEncoder
import numpy as np
from tensorflow.keras import utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout


'''
Permet d'attribuer l'allocation dynamique de mémoire pour éviter les depassements
'''
import tensorflow as tf

class train():
        def __init__(self):
                self.i=1
                pass

        def train_model(self,data):

                data1 = shuffle(data)

                self.data1=data
                # On verifie que le dataset est équilibré et que les classes soient bien conformes
                print('DIMENSION DU DATASET')
                print(data.shape)

                print('EQUILIBRE DU DATASET')
                #print(data['result'].value_counts())
                print(data['sentiment'].value_counts())


                # Definition des callbacks
                early = EarlyStopping(monitor='val_loss', min_delta=0, patience=2, verbose=0, mode='auto')
                check = ModelCheckpoint('model.hdf5', monitor='val_loss', verbose=0,save_best_only=True, save_weights_only=False, mode='auto')
                csvLogger = CSVLogger('log.csv', append=False, separator=',')


                # Definition des jeux de train et test
                trainSize = int(len(data) * .8)
                print ("Train taille: %d" % trainSize)
                print ("Test taille: %d" % (len(data) - trainSize))

                trainText = data["statement"][2:trainSize]
                trainResult = data["sentiment"][2:trainSize]

                #trainText = data[0][:trainSize]
                #trainResult = data[1][:trainSize]

                self.testText = data['statement'][trainSize:]
                self.testResult = data['sentiment'][trainSize:]

                #self.testText = data[0][trainSize:]
                #self.testResult = data[0][trainSize:]

                # Fix des hyper parametres
                batch_size = 256
                epoch = 5
                maxWords = 1000

                # Transforme le text vers une matrice de mot et permet de lui donnée un indice
                self.tokenize = text.Tokenizer(num_words=maxWords, char_level=False)
                self.tokenize.fit_on_texts(trainText)

                self.xTrain = self.tokenize.texts_to_matrix(trainText)
                self.tokenize.fit_on_texts(self.testText)
                self.xTest = self.tokenize.texts_to_matrix(self.testText)


                #Défini les labels des prédictions
                encoder = LabelEncoder()
                encoder.fit(trainResult)
                self.yTrain = encoder.transform(trainResult)
                self.yTest = encoder.transform(self.testResult)
                numClasses = np.max(self.yTrain) + 1

                self.yTest = utils.to_categorical(self.yTest, numClasses)
                self.yTrain = utils.to_categorical(self.yTrain, numClasses)


                # Shape de nos donnees avant entrainement
                print('xTrain shape:', self.xTrain.shape)
                print('xTest shape:', self.xTest.shape)
                print('yTrain shape:', self.yTrain.shape)
                print('yTest shape:', self.yTest.shape)




                # Definition de notre modele
                self.model = Sequential()
                self.model.add(Dense(512, input_shape=(maxWords,)))
                self.model.add(Activation('relu'))
                self.model.add(Dropout(0.5))
                self.model.add(Dense(numClasses))
                self.model.add(Activation('softmax'))


                # Compilation du modele
                self.model.compile(loss='categorical_crossentropy',optimizer=keras.optimizers.Adamax(lr=0.001, beta_1=0.9, beta_2=0.999, decay=0.0),metrics=['accuracy'])

                self.model.summary()
                # Entrainement du modele
                train =  self.model.fit(self.xTrain, self.yTrain, epochs=epoch, callbacks = [csvLogger, early, check], batch_size=batch_size, validation_data=(self.xTest,self.yTest))
                print("entrainement est terminer")
        def tester1(self,label):
                res=self.model.evaluate(self.xTest,self.yTest)

                label.grid(row=0,column=0)
                label['text']="les resultat de l'entrainement est  :"+str(res[1]*100)+" %"


        def  tester(self,root,data2):
                pcount = 0
                ncount = 0
                un = 0
                zero = 0
                for v in data2['statement']:
                    print('herrre')
                    phrase = str(v)
                    #print(phrase)

                    tokens = self.tokenize.texts_to_matrix([phrase])
                    print(self.data1['statement'][0])
                    print(data2['statement'][0])

                    #print(list(self.data1['statement'])[list(data2['statement']).index(v)])


                    a = self.model.predict(np.array(tokens))
                    print(a)



                    if a[0][0]>a[0][1]:
                            pcount+=1

                    else:
                            ncount+=1
                print(pcount)
                print(ncount)

        def  simulation(self,v,frame,i):
                phrase = str(v)
                tokens = self.tokenize.texts_to_matrix([phrase])
                self.i+=1
                a = self.model.predict(np.array(tokens))
                print("super", a)
                print("herrre text",phrase)
                lbl = Label(frame, )
                lbl.grid(row=i+2,column=0)
                if a[0][0]>a[0][1]:
                        lbl['text']=phrase
                        lbl.configure(bg="green")
                else:
                        lbl['text'] = "votre commentaire a été supprimé"+" :"+phrase
                        lbl.configure(bg="red")


