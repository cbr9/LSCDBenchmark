import sys, os
import pandas as pd
import csv
from collections import defaultdict, Counter
from sklearn import metrics
from scipy import stats
import argparse
import itertools

# command line arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gold", help = "absolute path to the file containing gold data",required=True)
parser.add_argument("-p", "--predictions", help = "absolute path to the file containg predictions",required=True)
parser.add_argument("-agr", "--agreement", help = "absolute path to the file containing agreement statistics")
parser.add_argument("-o", "--out", help = "absolute path to the output folder",required=True)


args = parser.parse_args()
gold_file = args.gold
predictions_file = args.predictions
output_dir = args.out
computed_scores = []

def compute_score(gold,predictions,evaltype):
    results = defaultdict(lambda: 0.0)
    if evaltype == 'change_graded':
        results[evaltype] = [('spearmanr',str(stats.spearmanr(gold,predictions)).strip('SpearmanrResult'))]
    else:
        accuracy = float(metrics.accuracy_score(gold,predictions))
        f1_score = float(metrics.f1_score(gold,predictions))
        recall_score = float(metrics.recall_score(gold,predictions))
        precision = float(metrics.precision_score(gold,predictions))
        results[evaltype] = [('accuracy',accuracy),('f1_score',f1_score),('recall_score',recall_score),('precision',precision)]

    return results


# load golde
golddata = pd.read_csv(gold_file,delimiter='\t',quoting=csv.QUOTE_NONE)

# load predictions
preddata = pd.read_csv(predictions_file,delimiter='\t',quoting=csv.QUOTE_NONE)


assert os.path.exists('scorer.conf')
config_dict = {l.strip().split('\t')[0]:l.strip().split('\t')[1:] for l in open('scorer.conf').readlines()}
print(config_dict)
if config_dict['evaluation_type']:
    evaltypes = config_dict['evaluation_type']
else:
    evaltypes = ["change_binary","change_binary_gain","change_binary_loss","change_graded"]

for evaltype in evaltypes:
    if config_dict['filter_threshold'] and config_dict['filter_label']:
        if args.agreement:
            stats_agreement = pd.read_csv(args.agreement,delimiter='\t',quoting=csv.QUOTE_NONE)

            for (fl,thr) in itertools.product(config_dict['filter_label'],config_dict['filter_threshold']):
                filtered_data = stats_agreement.loc[(stats_agreement[fl] >= float(thr))]
                gold = golddata.loc[golddata['lemma'].isin(filtered_data['data'])].get([evaltype])
                pred = preddata.loc[preddata['lemma'].isin(filtered_data['data'])].get([evaltype])
                score = compute_score(gold,pred,evaltype)
                computed_scores.append((str(fl),str(thr),score))

        else:
            print('-agr/--agreement argument is required')
            exit()
    else:
        gold = golddata.get([evaltype])
        pred = preddata.get([evaltype])
        score = compute_score(gold,pred,evaltype)
        computed_scores.append(('no-cleaning','no-cleaning',score))
        #print(len(gold),len(pred))

#[compute_score(gold,predictions,evaltype) for evaltype in evaltypes]


# output
with open(output_dir + '/results_summary.csv', 'w') as f:
    for (fl,thr,results) in computed_scores:
        f.write(str('filter='+fl+'\t'+'threshold='+thr)+'\n')
        for evaltype in results:
            f.write('EvaluationType='+evaltype+'\n')
            f.write('\t'.join([p+'='+str(v) for (p,v) in results[evaltype]]+['\n\n']))
            print(fl,thr,evaltype,results[evaltype])
