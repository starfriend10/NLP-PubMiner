# -*- coding: utf-8 -*-
"""
@initial preparation: 2020
@latest revision: 2025
@author: Junjie Zhu
@purpose: Utilize NLP text mining methods to identify relevant research articles for data mining #part II
##the code was prepared based on publication records from the Web of Science
##the methods were applied to numerious studies, and the text mining aglorithem was initially developed for Zhu et al. (2021):
"Zhu, J. J., Dressel, W., Pacion, K., & Ren, Z. J. (2021). ES&T in the 21st century: a data-driven analysis of research topics, 
interconnections, and trends in the past 20 years. Environmental Science & Technology, 55(6), 3453-3464."

"""

import numpy as np
import pandas as pd
from nltk import SnowballStemmer

stemmer = SnowballStemmer("english")
def nat_lang(strng):
    strng = strng.lower()
    if len(strng) > 4:
        word = stemmer.stem(strng)
    else:
        word = strng
    return word

#####wastewater data###############################################################
df0 = pd.read_csv(r'01 Preprocessed publication data.csv') #retrieve the preprocessed publication data
df1 = df0[['PY', 'DE', 'TI', 'AB', 'DT', 'SO', 'AU', 'RP', 'DI', 'termsa', 'termsb']] #other fields like article type, journal name, author list, DOI if additional inventory is needed


#####key terms prepared#############################################################
keywordlist01 = ['keyword 1', 'another keyword 2', 'another keyword 3'] #change the keywords as needed to refine the identification
keywordlist02 = ['keyword a', 'another keyword b', 'another keyword c'] #change the keywords as needed to refine the identification
#keywordlist03 = ['keyword i', 'another keyword ii', 'another keyword iii'] #you can add additional lists of keywords as needed


keywordlist1 = [nat_lang(w) for w in keywordlist01 if len(w)>2]
keywordlist2 = [nat_lang(w) for w in keywordlist02 if len(w)>2]

df2 = df1.reset_index().drop(['index'], axis = 1)
df2.iloc[:, -1].replace(np.nan, '', inplace = True) #in case there is a nan
df2.iloc[:, -2].replace(np.nan, '', inplace = True) #in case there is a nan


lst_pub = []
for i in range(len(df2)):
    listwords1 = df2.iloc[i, -1].split('; ')
    listwords2 = df2.iloc[i, -2].split('; ')
    listwords = listwords1 + listwords2
    if any(i in keywordlist1 for i in listwords) and any(i in keywordlist2 for i in listwords): #set your screening rule based on your needs
        lst_pub.append(i)

df_topic = df2[df2.index.isin(lst_pub)].reset_index().drop(['index'], axis = 1) #get your first relevant publication list

df_topic.to_csv('02 Initial preprocessed data.csv', index = False) #save the initial list


##stop here if there are only a few publications in your initial list and change the previous keywords to boost your results
##proceed to the following session if the initial list is huge and you want to screen out irrelevant publication to reduce the labor load for expert data retrieval

###remove irrelevant data#######################################################

from nltk.tokenize import word_tokenize

#anti-keywords
lst_irre = ['keyword x', 'another keyword y', 'another keyword z'] #change the anti-keywords as needed to refine the anti-identification
lst_irre2 = [nat_lang(w) for w in lst_irre]

def irre_ct(df):
    listwords1 = df.iloc[i, -1].split('; ')
    listwords2 = df.iloc[i, -2].split('; ') 
    listwords = listwords1 + listwords2    
    if any(i in lst_irre2 for i in listwords):
        kwlist1 = word_tokenize(df.iloc[i, 3])
        kwlist2 = [nat_lang(w) for w in kwlist1]
        counts = [kwlist2.count(w) for w in lst_irre2]
        sumcts = sum(counts) #count the frequency of a anti-keywords
    else:
        sumcts = 0
    return sumcts


lst_irre = []
lst_re = []
for i in range(len(df_topic)):
    sumcts = irre_ct(df_topic)
#A low frequency increases the size of irrelevant publications but may remove some relevant publications; vice verse.
    if sumcts >= 2: #frequency of anti-keywords, default is set as 2. 
        lst_irre.append(i)
    else:
        lst_re.append(i)        

df_topic_irre = df_topic[df_topic.index.isin(lst_irre)].reset_index().drop(['index'], axis = 1) #irrelevant list in case you want to check to refine your anti-keywords and frequency
df_topic2 = df_topic[df_topic.index.isin(lst_re)].reset_index().drop(['index'], axis = 1)

df_topic2.to_excel('03 Final preprocessed data.xlsx', index = False) #save the final list


