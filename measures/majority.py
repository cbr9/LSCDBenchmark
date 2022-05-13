# the code is adopted from https://github.com/Garrafao/LSCDetection/blob/master/measures/rand.py
import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
from collections import Counter


def majority(targets,data,path_results):
    """
    Measure assigning majority class label to targets (as baseline).
    """

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # find majority class
    majority_val = max(Counter(list(data['change_binary'])))

    # save majority labels to the output file
    with open(path_results, 'w', encoding='utf-8') as f_out:
        for t in targets:
                f_out.write('\t'.join((t, str(majority_val)+'\n')))
    f_out.close()


    logging.info("--- %s seconds ---" % (time.time() - start_time))
