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
parser.add_argument("-ft", "--filtertype", help = "filter type either hard or soft")
parser.add_argument("-fl", "--filterlabel", help = "filter label (e.g. kri_full)")
parser.add_argument("-et", "--evaltype", help = "evaluation type e.g. change_binary")
parser.add_argument("-agr", "--agreement", help = "absolute path to the file containing agreement statistics")
parser.add_argument("-o", "--out", help = "absolute path to the output folder",required=True)


args = parser.parse_args()
gold_file = args.gold
predictions_file = args.predictions
output_dir = args.out

# load golde
golddata = pd.read_csv(gold_file,delimiter='\t',quoting=csv.QUOTE_NONE)

# load predictions
preddata = pd.read_csv(predictions_file,delimiter='\t',quoting=csv.QUOTE_NONE)

results = defaultdict(lambda: 0.0)

if args.evaltype:
    evaltypes = [args.evaltype]
else:
    evaltypes = ["change_binary","change_binary_gain","change_binary_loss","change_graded"]

if args.filtertype and args.filterlabel:
    if args.filtertype == 'hard':
        threshold = 0.3
    elif args.filtertype == 'soft':
        threshold = 0.1
    if args.agreement:
        agreement_stats_file = args.agreement
        stats_agreement = pd.read_csv(agreement_stats_file,delimiter='\t',quoting=csv.QUOTE_NONE)
        filtered_data = stats_agreement.loc[(stats_agreement[args.filterlabel] >= threshold)]
        #gold = golddata.loc[golddata['lemma'].isin(filtered_data['data'])].get(['lemma',evaltype])
        #predictions = preddata.loc[preddata['lemma'].isin(filtered_data['data'])].get(['lemma',evaltype])
        golddata = golddata.loc[golddata['lemma'].isin(filtered_data['data'])]
        preddata = preddata.loc[preddata['lemma'].isin(filtered_data['data'])]

    else:
        print('-agr/--agreement argument is required')
        exit()


# check for validity of evaluation type
for evaltype in evaltypes:
    if evaltype not in golddata.columns.values or evaltype not in preddata.columns.values:
        print('Invalid evaluation type or the score is not available for this data set')
        exit()
    gold = golddata.get([evaltype])
    predictions = preddata.get([evaltype])
    #print(len(gold),len(predictions))

# scores computation

    if evaltype == 'change_graded':
        results[(evaltype,'spearmanr')] = str(stats.spearmanr(gold,predictions)).strip('SpearmanrResult')
    else:
        results[(evaltype,'accuracy')] = float(metrics.accuracy_score(gold,predictions))
        results[(evaltype,'f1_score')] = float(metrics.f1_score(gold,predictions))
        results[(evaltype,'recall_score')] = float(metrics.recall_score(gold,predictions))
        results[(evaltype,'precision')] = float(metrics.precision_score(gold,predictions))

# output
with open(output_dir + '/results_summary.csv', 'w') as f:
    w = csv.DictWriter(f, list(results.keys()), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerow(results)
