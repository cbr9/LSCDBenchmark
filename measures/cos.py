import logging
import sys
sys.path.append('/Users/xvirsh/shafqat/postDoc-Swe/project2022/LSCDiscovery-main/modules')
import time

from docopt import docopt
import numpy as np
from scipy.spatial.distance import cosine as cosine_distance

from utils_ import Space

def cos(space1,space2):
    """
    Compute cosine distance for targets in two matrices.
    """
    print(space1)
    # Get the arguments

    #path_matrix1 = args['<path_matrix1>']
    #path_matrix2 = args['<path_matrix2>']
    #path_targets = args['<path_targets>']
    #path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load matrices and rows
    #try:
    #    space1 = Space(path_matrix1, format='npz')
    #except ValueError:
    #    space1 = Space(path_matrix1, format='w2v')
    #try:
    #    space2 = Space(path_matrix2, format='npz')
    #except ValueError:
    #    space2 = Space(path_matrix2, format='w2v')

    matrix1 = space1.matrix
    row2id1 = space1.row2id
    matrix2 = space2.matrix
    row2id2 = space2.row2id

    distances = {}

    # Usage 1: compute CD for every word in the intersection of the vocabularies
    #if path_targets == None:

        # Compute CD
    print(row2id1)
    for key in row2id1:
            try:
                vec1 = matrix1[row2id1[key]].toarray().flatten()
                vec2 = matrix2[row2id2[key]].toarray().flatten()
                cd = cosine_distance(vec1, vec2)
                distances[key] = cd
            except KeyError:
                pass
    # Usage 2: compute CD for every word in <path_targets>
    '''else:
        # Load targets
        with open(path_targets, 'r', encoding='utf-8') as f:
            targets = [line.strip() for line in f]

        # Compute CD
        for word in targets:
            try:
                vec1 = matrix1[row2id1[word]].toarray().flatten()
                vec2 = matrix2[row2id2[word]].toarray().flatten()
                cd = cosine_distance(vec1, vec2)
                distances[word] = cd
            except KeyError:
                distances[word] = 'nan'
                continue

    # Write output to <paht_output>
    with open(path_output, 'w', encoding='utf-8') as f:
        for key in distances:
            f.write(key + '\t' + str(distances[key]) + '\n')'''
    for key in distances:
        print(key,distances[key])

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")
    return(distances)
