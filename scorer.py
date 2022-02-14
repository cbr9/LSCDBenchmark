import sys
import pandas as pd
import csv
from collections import defaultdict, Counter
from sklearn import metrics
from scipy import stats
import argparse

# command line arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gold", help = "absolute path to the file containing gold data",required=True)
parser.add_argument("-p", "--predictions", help = "absolute path to the file containg predictions",required=True)
parser.add_argument("-f", "--filter", help = "filter label (e.g. kri_full)")
parser.add_argument("-et", "--evaltype", help = "evaluation type e.g. change_binary",required=True)
parser.add_argument("-o", "--out", help = "absolute path to the output folder",required=True)
parser.add_argument("-agr", "--agreement", help = "absolute path to the file containing agreement statistics")

args = parser.parse_args()
gold_file = args.gold
predictions_file = args.predictions
evaltype = args.evaltype
output_dir = args.out

# load golde
golddata = pd.read_csv(gold_file,delimiter='\t',quoting=csv.QUOTE_NONE)

# load predictions
preddata = pd.read_csv(predictions_file,delimiter='\t',quoting=csv.QUOTE_NONE)

# check for validity of evaluation type
if evaltype not in golddata.columns.values or evaltype not in preddata.columns.values:
    print('Invalid evaluation type or the score is not available for this data set')
    exit()

# load stats_agreement data and filter it
if args.filter:
    if args.agreement:
        agreement_stats_file = args.agreement
        stats_agreement = pd.read_csv(agreement_stats_file,delimiter='\t',quoting=csv.QUOTE_NONE)
        filtered_data = stats_agreement.loc[(stats_agreement['kri_full'] >= 0.3)]
        gold = golddata.loc[golddata['lemma'].isin(filtered_data['data'])].get(['lemma',evaltype])
        predictions = preddata.loc[preddata['lemma'].isin(filtered_data['data'])].get(['lemma',evaltype])
    else:
        print('-agr/--agreement argument is required')
        exit()
else:
    gold = golddata.get(['lemma',evaltype])
    predictions = preddata.get(['lemma',evaltype])

# scores computation
results = defaultdict(lambda: 0.0)
if evaltype == 'change_graded':
    results['spearmanr'] = stats.spearmanr(gold[evaltype],predictions[evaltype])
else:
    results['accuracy'] = float(metrics.accuracy_score(gold[evaltype],predictions[evaltype]))
    results['f1_score'] = float(metrics.f1_score(gold[evaltype],predictions[evaltype]))
    results['recall_score'] = float(metrics.recall_score(gold[evaltype],predictions[evaltype]))

# output
with open(output_dir + '/results_summary.csv', 'w') as f:
    w = csv.DictWriter(f, list(results.keys()), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerow(results)
