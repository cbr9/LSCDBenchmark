# the code is adopted from https://github.com/Garrafao/LSCDetection/blob/master/measures/rand.py
import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import random

def rand(targets,random_scores_targets_path,is_rel):
    """
    Measure assigning random values to targets (as baseline).
    """

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # random scores
    scores = {}
    for t in targets:
        if is_rel:
            score = random.uniform(0, 1)
        scores[t] = score


    # save random scores to the output file
    with open(random_scores_targets_path, 'w', encoding='utf-8') as f_out:
        for t in targets:
                f_out.write('\t'.join((t, str(scores[t])+'\n')))
    f_out.close()


    logging.info("--- %s seconds ---" % (time.time() - start_time))
