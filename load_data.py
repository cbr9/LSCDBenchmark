import sys
import pandas as pd
import csv
from collections import defaultdict, Counter
from sklearn import metrics
from scipy import stats
import argparse
import os

def load_data(data_path=None,lemma=None,preprocessing='context'):
    assert data_path != None, 'Data path is required'

    if lemma != None:
        lemmas = [l for l in os.listdir(data_path+'/data') if l.split('_')[0] == lemma]
    else:
        #print(os.listdir(data_path+'/data'))
        lemmas = os.listdir(data_path+'/data')
    data = []
    for lemma_dir in lemmas:
        csvfile = data_path + '/data/' + lemma_dir + '/uses.csv'
        df = pd.read_csv(csvfile,delimiter='\t',quoting=csv.QUOTE_NONE)
        data.append(list(df.get(['lemma','identifier','date',preprocessing]).to_records(index=False)))

    return(data)

if __name__ == "__main__":
    #data = load_data(lemma='attack',data_path='./usage-graph-data/dwug_en/')
    #data = load_data(lemma='attack',data_path='./usage-graph-data/dwug_en/',preprocessing='context_tokenized')
    data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context_tokenized')
    #data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context_pos')
    #data = load_data(preprocessing='context_tokenized')
    print(data)
