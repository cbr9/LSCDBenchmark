import csv
import gzip
import logging
import sys, os
import yaml
sys.path.append('./modules')
sys.path.append('./measures/')

from binary2 import *
from rand import *
#from bert2 import *


def random_baseline():
        # read configurations
        assert os.path.exists('baseline.yaml')
        with open("baseline.yaml", 'r') as config:
            configurations = yaml.safe_load(config)
        config_dict = configurations['random']
        print(config_dict)

        is_rel = config_dict['is_rel']
        path_results = config_dict['path_results']
        target_words_path = config_dict['path_targets']
        language = config_dict['language']

        # target words
        # a hack to produce a target_words lists, standard is to have a list of words at 'target_words_path' as is the case for English
        target_words = os.listdir('./usage-graph-data/dwug_'+language+'/data/')

        #target_words = [w.strip().split('_')[0] for w in open(target_words_path+'/target_words.txt').readlines()][:]

        random_scores_targets_path = path_results+'/rand/random_scores_targets.tsv'

        # random scores
        rand(target_words,random_scores_targets_path,is_rel)

        # binary classification
        binary(path_results+'rand/random_scores_targets.tsv',path_results+'rand/scores_targets.tsv')



if __name__ == "__main__":
    random_baseline()
