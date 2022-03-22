import csv
import logging
import time

from docopt import docopt
import numpy as np

def binary(dis):
    path_targets = None
    #path_targets = args['<path_targets>']
    #path_output = args['<path_output>']
    t = 0.1

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load data
    distances = {}

    for (l,d) in dis:
            #try:
                distances[l] = float(d)
            #except ValueError:
            #    pass

    # Compute mean, std and threshold
    list_distances = np.array(list(distances.values()))
    print(list_distances)

    mean = np.mean(list_distances, axis=0)
    std = np.std(list_distances, axis=0)
    threshold = mean + t * std

    # Usage 1: discover changing words
    if path_targets == None:
        changing_words = []
        for key in distances:
            if distances[key] >= threshold:
                changing_words.append(key)

        # Write changing words to <path_output>
        #with open(path_output, 'w', encoding='utf-8') as f:
        #for word in changing_words:
                #f.write(word + '\n')
        print(changing_words)

    # Usage 2: label target words according to threshold (binary classification)
    '''else:
        # Load data
        target_distances = {}
        with open(path_targets, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
            for row in reader:
                try:
                    target_distances[row[0]] = float(row[1])
                except ValueError:
                    pass

        # Compute binary scores
        binary_scores = {}
        for key in target_distances:
            if target_distances[key] >= threshold:
                binary_scores[key] = 1
            else:
                binary_scores[key] = 0

        # Write binary scores to <path_output>
        with open(path_output, 'w', encoding='utf-8') as f:
            for key, value in binary_scores.items():
                f.write(key + '\t' + str(value) + '\n')'''


    logging.info("--- %s seconds ---" % (time.time() - start_time))