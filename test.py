

import pandas as pd

col_names = ['text', 'result']
allData = pd.DataFrame(columns=col_names)
data=pd.read_csv('french_tweets.csv',header=None)



for i in range(50000):

     allData = allData.append(pd.DataFrame({'text':data[1][150002+i],'result':data[0][150002+i]}, index=[0]))
     allData = allData.append(pd.DataFrame({'text':data[1][i+768308+150002],'result':data[0][i+768308+150002]}, index=[0]))


allData.to_csv('french4.txt', header=['text', 'result'], index=None, sep=',', mode='a')
