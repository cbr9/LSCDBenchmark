import sys
import os
import csv
from collections import defaultdict
from sklearn.metrics.cluster import adjusted_rand_score
import numpy as np

def sense_description_scorer(gold, pred):

    variable_names = list(gold[0].keys())
    variable_names.remove('identifier')
    for name in variable_names:
        # to do: distinguish variable names (this is a bug)
        identifiers_gold = [row['identifier'] for row in gold]
        identifiers_pred = [row['identifier'] for row in pred]
        if set(identifiers_gold)!=set(identifiers_pred) or len(identifiers_gold)!=len(identifiers_pred) or len(identifiers_gold)!=len(set(identifiers_gold)):
            print('Skipping. Prediction identifiers different from gold or duplicate identifiers.')
            return np.NaN
        identifier2gold = {row['identifier']:row[name] for row in gold}
        identifier2pred = {row['identifier']:row[name] for row in pred}
        variable_gold = [identifier2gold[identifier] for identifier in identifiers_gold if identifier2gold[identifier]!='nan'] # skip nan values in gold
        variable_pred = [identifier2pred[identifier] for identifier in identifiers_gold if identifier2gold[identifier]!='nan'] # skip nan values in gold
        if 'nan' in variable_pred:
            print('Skipping. Prediction contains nan.')
            return np.NaN        
        ari = adjusted_rand_score(variable_gold, variable_pred)           
    
    return ari, 'ARI'

evaltype2scorer = {'sense_description':sense_description_scorer}

[_ ,testsets, predictions, outfolder] = sys.argv

results = []
print('Reading gold and predictions.')
for root, subdirectories, files in os.walk(testsets):
    for f in files:
        path = os.path.join(root, f)
        _, dataset, evaltype, data = path.split('/')
        print(dataset, evaltype, data)
        # Load gold
        with open(path, encoding='utf-8') as csvfile: 
            reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
            prediction = [row for row in reader]
        # Load predictions
        try:
            with open('/'.join([predictions, dataset, evaltype, data]), encoding='utf-8') as csvfile: 
                reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
                gold = [row for row in reader]
        except FileNotFoundError:
            print('Skipping. No predictions provided.')
            continue
        scorer = evaltype2scorer[evaltype]
        score, metric = scorer(gold, prediction)
        results.append((dataset, evaltype, data.split('.')[0], score, metric))

output_data_full = [{'dataset':dataset, 'evaltype':evaltype, 'data':data, 'score':score, 'metric':metric} for (dataset, evaltype, data, score, metric) in results]

dataset2evaltype2results = defaultdict(lambda: defaultdict(lambda: []))
for (dataset, evaltype, data, score, metric) in results:
    dataset2evaltype2results[dataset][evaltype].append((dataset, evaltype, data, score, metric))

output_data_summary = []
print('Calculating final results.')
for dataset, evaltype2results in dataset2evaltype2results.items():
    for evaltype, results in evaltype2results.items():
        print(dataset, evaltype, len(results), 'scores')
        if evaltype == 'sense_description':
            scores = np.array([score for (_, _, _, score, metric) in results])
            if np.isnan(scores).any():
                print('Skipping averaging. Some predictions missing.')                
            score = np.mean(scores)
            output_data_summary.append({'dataset':dataset, 'evaltype':evaltype, 'data':'average', 'score':score, 'metric':metric})
        elif len(results)==1:
            _, _, data, score, metric = results[0]
            output_data_summary.append({'dataset':dataset, 'evaltype':evaltype, 'data':data, 'score':score, 'metric':metric})
        else:
            output_data_summary.append({'dataset':' ', 'evaltype':' ', 'data':' ', 'score':' ', 'metric':' '})
            print('Something went terribly wrong.')

with open(outfolder + '/results_full.csv', 'w') as f:  
    w = csv.DictWriter(f, output_data_full[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(output_data_full)

with open(outfolder + '/results_summary.csv', 'w') as f:  
    w = csv.DictWriter(f, output_data_summary[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(output_data_summary)

