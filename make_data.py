import sys
import os
from pandas import DataFrame
import numpy as np
from pathlib import Path
import csv
from collections import defaultdict, Counter
from itertools import combinations

[_, folder, dataset, outfolder] = sys.argv

if dataset == 'dwug_de':

    # Extract majority labels from sense description annotation
    judgments_senses = []
    data_senses = []
    print(folder)
    for root, subdirectories, files in os.walk(folder + '/data'):
        for f in files:
            path = os.path.join(root, f)
            if f=='judgments_senses.csv':
                with open(path, encoding='utf-8') as csvfile: 
                    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
                    table = [row for row in reader]
                    judgments_senses = judgments_senses + table
            if f=='senses.csv':
                with open(path, encoding='utf-8') as csvfile: 
                    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
                    table = [row | {'lemma':path.split('/')[-2]} for row in reader]
                    data_senses = data_senses + table

    # Transform data            
    annotators = sorted(list(set([row['annotator'] for row in judgments_senses])))
    lemma2identifier2annotator2judgment = defaultdict(lambda: defaultdict(lambda: {}))
    for row in judgments_senses:
        lemma2identifier2annotator2judgment[row['lemma']][row['identifier']] |= {row['annotator']:row['identifier_sense']}

    # Get sense labels
    lemma2label2description = defaultdict(lambda: {})
    for row in data_senses:
        lemma2label2description[row['lemma']] |= {row['identifier_sense']:row['description_sense']}
    
    # Extract majority labels
    def extract_majority_label(judgments, threshold):
        label2count = Counter(judgments)
        majority_labels = [l for l, c in label2count.items() if c >= threshold]
        if len(majority_labels) > 0:
            label = np.random.choice(majority_labels)
        else:
            label = np.NaN  
        return label    

    lemma2identifier2maj2value = defaultdict(lambda: defaultdict(lambda: {}))
    for lemma, identifier2annotator2judgment in lemma2identifier2annotator2judgment.items():
        for identifier, annotator2judgment in identifier2annotator2judgment.items():
            judgments = list(annotator2judgment.values())
            is_andere = [True for j in judgments if j!='None' and lemma2label2description[lemma][j] == 'andere']
            judgments = [j if j!='None' else np.NaN for j in judgments] # set non-annotated instances to NaN
            for threshold in [2, 3]:
                if is_andere:
                    lemma2identifier2maj2value[lemma][identifier]['maj_'+str(threshold)] = np.NaN # ignore instances having any andere judgment
                else:
                    lemma2identifier2maj2value[lemma][identifier]['maj_'+str(threshold)] = extract_majority_label(judgments, threshold)
            
    print(lemma2identifier2maj2value)
    
    # Export data
    for lemma in lemma2identifier2maj2value.keys():
        output_folder = outfolder + '/' + dataset + '/' + 'sense_description'
        #print(lemma2identifier2maj2value[lemma])
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_data = [{'identifier':identifier} | {maj:value for maj, value in maj2value.items()} for identifier, maj2value in lemma2identifier2maj2value[lemma].items()]                
        with open(output_folder + '/' + lemma + '.csv', 'w') as f:  
            w = csv.DictWriter(f, output_data[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
            w.writeheader()
            w.writerows(output_data)

