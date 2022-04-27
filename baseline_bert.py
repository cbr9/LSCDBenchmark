import csv
import gzip
import logging
import sys
sys.path.append('/Users/xvirsh/shafqat/postDoc-Swe/project2022/LSCDiscovery-main/modules')
sys.path.append('./measures/')
sys.path.append('./contextualized/')

import numpy as np
import random
from scipy.spatial.distance import cosine as cosine_distance

from load_data import *
from cos import *
from binary import *
from apd import *
from bert import *

def bert_baseline():
        assert os.path.exists('baseline.conf')
        config_dict = {l.strip().split('\t')[0]:l.strip().split('\t')[1:] for l in open('baseline.conf').readlines()}
        print(config_dict)
        language = config_dict['language'][0]
        type_sentences = config_dict['type_sentences'][0]
        layers = config_dict['layers'][0]
        is_len = config_dict['is_len'][0]
        #path_output = config_dict['path_output'][0]
        target_words = ['afternoon','attack','bag','ball']
        test_sentences1 = []
        test_sentences2 = []
        sentences_vectors1 = []
        sentences_vectors2 = []
        for target_word in target_words:
            data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context',lemma=target_word)
            #for d in data[0]:
            #    print(d)
            #    print('\n\n')
            #print(data)
            for (lemma,identifier,date,grouping,preprocessing,context_tokenized,indexes_target_token_tokenized,context_lemmatized) in data[0]:
                #print(lemma)
                if grouping == 1:
                    test_sentences1.append({'lemma':lemma.split('_')[0],'sentence_lemma':context_lemmatized,'index_lemma':indexes_target_token_tokenized,'index_token':indexes_target_token_tokenized,'sentence_token':context_tokenized})
                elif grouping == 2:
                    test_sentences2.append({'lemma':lemma.split('_')[0],'sentence_lemma':context_lemmatized,'index_lemma':indexes_target_token_tokenized,'index_token':indexes_target_token_tokenized,'sentence_token':context_tokenized})
            sentences_vectors1.append(bert(test_sentences1,target_word,language,type_sentences,layers,is_len))
            sentences_vectors2.append(bert(test_sentences2,target_word,language,type_sentences,layers,is_len))
        #distances_apd = [(l1,apd(space1,space2)) for (l1,space1),(l2,space2) in zip(sentences_vectors1,sentences_vectors2)]
        distances_cos = [(l1,cos(space1,space2)) for (l1,space1),(l2,space2) in zip(sentences_vectors1,sentences_vectors2)]
        #print(distances_cos,'distances')
        #binary(distances_apd)
        binary(distances_cos)



if __name__ == "__main__":
    #data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context_tokenized')
    #data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context_pos')
    bert_baseline()
