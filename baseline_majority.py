import csv
import gzip
import logging
import sys, os
import yaml
import pandas as pd
sys.path.append('./modules')
sys.path.append('./measures/')

from binary2 import *
from majority import *
#from bert2 import *


def majority_baseline():
        # read configurations
        assert os.path.exists('baseline.yaml')
        with open("baseline.yaml", 'r') as config:
            configurations = yaml.safe_load(config)
        config_dict = configurations['majority']
        print(config_dict)

        language = config_dict['language']
        path_results = config_dict['path_results']
        target_words_path = config_dict['path_targets']
        data_path = config_dict['path_data']

        # target words
        # a hack to produce a target_words lists, standard is to have a list of words at 'target_words_path' as is the case for English
        target_words = os.listdir('./usage-graph-data/dwug_'+language+'/data/')

        #target_words = [w.strip().split('_')[0] for w in open(target_words_path+'/target_words.txt').readlines()][:]

        data = pd.read_csv(data_path+'dwug_'+language+'/stats/opt/stats_groupings.csv',delimiter='\t',quoting=csv.QUOTE_NONE)
        data['lemma'] = data['lemma'].str.replace('_(\w+)','',regex=True) # remove trailing pos tag with target words

        # random scores
        majority(target_words,data,path_results+'majority/scores_targets.tsv')

        # binary classification
        #binary(path_results+'rand/random_scores_targets.tsv',path_results+'rand/scores_targets.tsv')



if __name__ == "__main__":
    majority_baseline()
