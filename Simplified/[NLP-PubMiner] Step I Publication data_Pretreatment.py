# -*- coding: utf-8 -*-
"""
@initial preparation: 2020
@latest revision: 2025
@author: Junjie Zhu
@purpose: Utilize NLP text mining methods to identify relevant research articles for data mining #part I
##the code was prepared based on publication records from the Web of Science
##the methods were applied to numerious studies, and the text mining aglorithem was initially developed for Zhu et al. (2021):
"Zhu, J. J., Dressel, W., Pacion, K., & Ren, Z. J. (2021). ES&T in the 21st century: a data-driven analysis of research topics, 
interconnections, and trends in the past 20 years. Environmental Science & Technology, 55(6), 3453-3464."

"""

import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk import SnowballStemmer
from pathlib import Path

##import text documents
path = Path(r'X:/Your project folder/Your raw text data folder/') #your data folder
alltxts = path.rglob("*.txt") #retrieve all raw text document

#create a new csv data table
data = []
for filename in alltxts:
    #table = pd.read_csv(filename, sep='\t', index_col=False, header=0, error_bad_lines=False) #(Deprecated, pandas < 1.3.0)
    table = pd.read_csv(filename, sep='\t', index_col=False, header=0, on_bad_lines='skip') #(Newer, pandas ≥ 1.3.0)
    data.append(table)

df = pd.concat(data, axis=0, ignore_index=True)

#exclude irrelevant data columns
df1 = df.drop(['PT','BA', 'BE', 'GP', 'BF', 'CA', 'SE', 'BS', 'CT', 'CY',
               'CL', 'SP', 'HO', 'FU', 'FX', 'PU', 'PI', 'PA', 'SN', 'EI', 'BN',
               'J9', 'JI', 'PN', 'SU', 'SI', 'MA', 'AR', 'D2', 'EA', 'WC', 'SC',
               'GA', 'PM', 'OA', 'HC', 'HP'], axis = 1)

df2 = df1.reset_index().drop(['index'], axis = 1) #reset index after concatenation

#only retain published data with valid year
lstwrng = []
for i in range(len(df2)):
    strng = str(df2['PY'][i])
    strng = strng.replace('.', '')
    if strng.isdigit() == False:
        lstwrng.append(i)

df3 = df2.drop(lstwrng) #dataframe after removing invalid data
df3del = df2.loc[lstwrng] #in case you want to inventory the invalid data

df3['PY'] = df3['PY'].astype(int)

#only retain published data with specified requirements
df3 = df3[(df3['PY'] >= 1900) & (df3['PY'] <= 2025) & (df3['LA'] == 'English')] #change years and language as you need

#sort data by year and volume/issue
df3 = df3.sort_values(by=['PY', 'VL', 'IS'])

#############################################
#Title, author keywords, and abstract; at least one of the three fields [title, author keywords, abstract] should be valid
df4 = df3[~((pd.isnull(df3['TI']) == True) & (pd.isnull(df3['DE']) == True) & (pd.isnull(df3['AB']) == True))]

#############################################
#get ready for the NLP data preprocessing
df_kw0 = df4.reset_index().drop(['index'], axis = 1)

#define a funtion of stemming
stemmer = SnowballStemmer("english")
def nat_lang(strng):
    strng = strng.lower()
    if len(strng) > 4: #change the length of string as you need
        word = stemmer.stem(strng)
    else:
        word = strng
    return word

# Function to generate n-grams from sentences
def extract_ngrams(data, num):
    n_grams = ngrams(nltk.word_tokenize(data), num)
    return [ ' '.join(grams) for grams in n_grams]


df_kw1 = df_kw0.replace(np.nan, '', regex=True)

#prepare stop words
nltk.download('stopwords') #one-time run, no need to repeat if it was downloaded
nltk.download('punkt_tab') #one-time run, no need to repeat if it was downloaded

stop_words = stopwords.words('english') #assume your're working on english, change language as you need


#define a function to remove common punctuations
def lst_clean(lst1):
    lst2 = [w for w in lst1 if w]
    lstpun = [',', '.', ' ', '/', "`", ';', ':', '<', '>', '=']
    del1 = []
    for w in lst2:
        if any(i in list(w[0]) for i in lstpun):
            del1.append(w)
    lst3 = [w for w in lst2 if w not in del1] #all generated ngrams, to split it into two columns for a big dataset
    lst3a = [w for w in lst3 if len(w.split(' ')) <= 2] #a new column includes ngrams = 1 or 2
    lst3b = [w for w in lst3 if len(w.split(' ')) > 2] #a new column includes ngrams = 3 or more
    return lst3a, lst3b



df_kw2 = df_kw1.copy(deep = True)
df_kw2['termsa'] = '' #the new column for ngrams = 1 or 2
df_kw2['termsb'] = '' #the new column for ngrams = 3 or more
for i in range(len(df_kw1)):
    kw = df_kw1.iloc[i, 6]
    ti = df_kw1.iloc[i, 2].replace('-', ' ') #replace hyphen in original title
    ab = df_kw1.iloc[i, 8].replace('-', ' ').replace('(', '').replace(')', '') #replace hyphen, brackets in original abstract
    at = (extract_ngrams(ti, 1) + extract_ngrams(ti, 2) + extract_ngrams(ti, 3) + extract_ngrams(ti, 4)
    + extract_ngrams(ab, 1) + extract_ngrams(ab, 2) + extract_ngrams(ab, 3) + extract_ngrams(ab, 4)) #ngrams from 1 to 4, but you can extend to a bigger number
    at2 = [w.lower() for w in at if not w in stop_words if len(w)>2] #remove stop words from the list of potential terms
    at3 = [w.replace('-', ' ') for w in at2] #replace hyphen again in generated terms from title and abstract
    kwlist = kw.split('; ') #author keywords if it has
    kwlist2 = [w.lower() for w in kwlist]
    kwlist3 = [word_tokenize(w) for w in kwlist2] #single words generated from author keywords
    kwlist4 = [w for sublist in kwlist3 for w in sublist]
    allterm = kwlist2 + kwlist4 + at3 #combine generated terms from title, abstract and keywords and original author keywords
    allterm2 = [w for w in allterm if w != []]
    allterm3 = [nat_lang(w) for w in allterm2] #stemming
    allterm3a, allterm3b = lst_clean(allterm3) #remove common punctuations
    alltermlsta = list(set(allterm3a))
    alltermlstb = list(set(allterm3b))
    alltermlsta2 = '; '.join(alltermlsta)
    alltermlstb2 = '; '.join(alltermlstb)
    df_kw2.iloc[i, -2] = alltermlsta2
    df_kw2.iloc[i, -1] = alltermlstb2 
    if i%1000 == 0:
        print(i)


df_kw2.to_csv('01 Preprocessed publication data.csv', index = False)






