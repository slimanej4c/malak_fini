import pandas as pd
import glob
import json
import numpy as np
#from tqdm import tqdm


# Template pour les soucis d'encodage
dict = {
    '\\u00e0': 'a',
    '\\u00e2': 'a',
    '\\u00e4': 'a',
    '\\u00C3': 'A',
    '\\u00C2': 'A',
    '\\u00C1': 'A',
    '\\u00C0': 'A',
    '\\u00c0': 'A',
    '\\u00e7': 'c',
    '\\u00c7': 'C',
    '\\u00e8': 'e',
    '\\u00e9': 'e',
    '\\u00ea': 'e',
    '\\u00eb': 'e',
    '\\u00c8': 'E',
    '\\u00C9': 'E',
    '\\u00c9': 'E',
    '\\u00CA': 'E',
    '\\u00CB': 'E',
    '\\u00ee': 'i',
    '\\u00ef': 'i',
    '\\u00ce': 'I',
    '\\u00CC': 'I',
    '\\u00CD': 'I',
    '\\u00CE': 'I',
    '\\u00CF': 'I',
    '\\u00f4': 'o',
    '\\u00f6': 'o',
    '\\u00D2': 'O',
    '\\u00D3': 'O',
    '\\u00D4': 'O',
    '\\u00D5': 'O',
    '\\u00D6': 'O',
    '\\u00f9': 'u',
    '\\u00fb': 'u',
    '\\u00fc': 'u',
    '\\u00D9': 'U',
    '\\u00DA': 'U',
    '\\u00DB': 'U',
    '\\u00DC': 'U',
    '\\u2019': "'",
    '\\u2018': "'",
    '\\u20ac': "euros",
    '&lt;': 'inferieur',
    '&le;': 'inferieur egale',
    '&gt;': 'superieur',
    '&ge;': 'superieur egale',
    '\\u00a0': '',
    '\\u00ab': "'",
    '\\u00bb': "'",
    ',': ' ',
    '\\ud83d': '',
    '\\ude09': '',
    '\\ude18': '',
    '\\ude08': '',
    '\n': ' ',
    '\r': ''
}



def cleanData(text, dict):
    '''
    Permet de nettoyer nos donnees
    :param text: une phrase
    :param dict: un dictionnaire de remplacement de donnees
    :return:
    '''
    for i, j in dict.items():
        text = text.replace(i, j)
    return text


def mergeAllTweet(chemin):
    '''
    Permet de merge l'ensemble des tweets positif et negatif dans un fichier unique
    :return:
    '''
    print("chemin",chemin)
    twitterFile1 = glob.glob(chemin[0])
    twitterFile2 = glob.glob(chemin[1])
    col_names = ['text', 'result']
    allData = pd.DataFrame(columns=col_names)
    save=chemin[2].replace("*",'')+"data.txt"



    #for file in tqdm(twitterFile):
    for file1 , file2  in zip(twitterFile1,twitterFile2):
        print('ok')
        fileOpened1 = open(file1, 'r').read()
        fileOpened2 = open(file2, 'r').read()
        jsonLine1 = json.loads(fileOpened1)
        jsonLine2 = json.loads(fileOpened2)
        cleanString1 = cleanData(jsonLine1['text'], dict)
        cleanString2 = cleanData(jsonLine2['text'], dict)

        allData = allData.append(pd.DataFrame({'text': cleanString1, 'result': 0}, index=[0]))
        allData = allData.append(pd.DataFrame({'text': cleanString2, 'result': 1}, index=[0]))


    allData.to_csv(save, header=None, index=None, sep=',', mode='a')


def cleanDuplicateData():
    '''
    Permet de supprimer les donnees en double
    :return:
    '''
    data = pd.read_csv('data.txt', sep=",", header=None)
    data.columns = ["text", "result"]
    print(data.shape)

    # Supprimer les row en doubles
    df2 = data.drop_duplicates(subset='text', keep="last").reset_index(drop=True)
    # Nb total de lignes

    #file = open('data.txt', 'w')
    #file.close()
    print(df2.shape)
    df2.to_csv('cleanData.txt', header=None, index=None, sep=',', mode='a')



