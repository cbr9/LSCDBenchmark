import csv
import gzip
import logging
import sys
sys.path.append('./modules')
sys.path.append('./measures/')
sys.path.append('./contextualized/')

import numpy as np
import random
from scipy.spatial.distance import cosine as cosine_distance

from load_data import *
from cos2 import *
from binary2 import *
from apd2 import *
from bert2 import *

def bert_baseline():
        assert os.path.exists('baseline.conf')
        config_dict = {l.strip().split('\t')[0]:l.strip().split('\t')[1:] for l in open('baseline.conf').readlines()}
        print(config_dict)
        language = config_dict['language'][0]
        type_sentences = config_dict['type_sentences'][0]
        layers = config_dict['layers'][0]
        is_len = config_dict['is_len'][0]
        path_output1 = config_dict['path_output1'][0]
        path_output2 = config_dict['path_output2'][0]
        path_results = config_dict['path_results'][0]
        target_words_path = config_dict['path_targets'][0]

        target_words = [w.strip().split('_')[0] for w in open(target_words_path+'/target_words.txt').readlines()][:]
        uses_corpus1 = []
        uses_corpus2 = []

        distance_targets_apd = open(path_results+'/apd/distance_targets.tsv','w')
        distance_targets_cos = open(path_results+'/cos/distance_targets.tsv','w')

        for target_word in target_words:
            print(target_word)
            data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context',lemma=target_word)
            for (lemma,identifier,date,grouping,preprocessing,context_tokenized,indexes_target_token_tokenized,context_lemmatized) in data[0]:
                if grouping == 1:
                    uses_corpus1.append({'lemma':lemma.split('_')[0],'sentence_lemma':context_lemmatized,'index_lemma':indexes_target_token_tokenized,'index_token':indexes_target_token_tokenized,'sentence_token':context_tokenized})
                elif grouping == 2:
                    uses_corpus2.append({'lemma':lemma.split('_')[0],'sentence_lemma':context_lemmatized,'index_lemma':indexes_target_token_tokenized,'index_token':indexes_target_token_tokenized,'sentence_token':context_tokenized})
            # bert vectors
            bert(uses_corpus1,target_word,language,type_sentences,layers,is_len,path_output1+target_word+'.tsv')
            bert(uses_corpus2,target_word,language,type_sentences,layers,is_len,path_output2+target_word+'.tsv')
            # apd and cos distances
            apd_distance = apd(path_output1+target_word+'.tsv',path_output2+target_word+'.tsv')
            distance_targets_apd.write(target_word+'\t'+str(apd_distance)+'\n')
            cos_distance = cos(path_output1+target_word+'.tsv',path_output2+target_word+'.tsv')
            distance_targets_cos.write(target_word+'\t'+str(cos_distance)+'\n')

        distance_targets_apd.close()
        distance_targets_cos.close()
        # binary classification
        binary(path_results+'apd/distance_targets.tsv',path_results+'apd/scores_targets.tsv')
        binary(path_results+'cos/distance_targets.tsv',path_results+'cos/scores_targets.tsv')



if __name__ == "__main__":
    #data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context_tokenized')
    #data = load_data(data_path='./usage-graph-data/dwug_en/',preprocessing='context_pos')
    bert_baseline()
