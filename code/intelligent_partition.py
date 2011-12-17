# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
from collections import defaultdict


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-r', '--test-data-ratio', dest='test_data_ratio', type=float, default=0.1,
        help='Ratio of data to be used for testing [default: 0.1]')
    parser.add_option('--train-fname', dest='train_fname', default='train.svm',
        help='Filename to save training vectors to')
    parser.add_option('--test-fname', dest='test_fname', default='test.svm',
        help='Filename to save testing vectors to')


    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        print 'Usage: %s [-r <ratio>] <vectors-filename>' % sys.argv[0]
        sys.exit(1)
    
    fname = args[0]
    
    f = open(fname, 'r')
    
    # Mapping of file id to vectors
    id_to_frags = defaultdict(list)

    # Note from Colin: Probably the reason this loop is causing OoM is that it requires putting the whole vector into memory. Fix idea: map, fragment ids to indices in the vector file, rather than a list of actual vectors. Then decide which ids are testing and training. Then iterate through vector file again, selectively copying to either the training or testing file.
    
    #this try-except block is to help us see when the 'Memory Error' is occuring with respect to how many lines are read
    counter=0
    try:
      for line in f:
	  print counter
	  counter += 1
	  vector, frag_id = line.split('#')
	  id_to_frags[frag_id.strip()].append(vector)
    except Exception as e:
      print e
	
    f.close()
    
    total_frags = sum( [len(id_to_frags[id_]) for id_ in id_to_frags] )
    ntest_frags = int(options.test_data_ratio*total_frags)
    
    test_f = open(options.test_fname, 'w')
    train_f = open(options.train_fname, 'w')
    
    for id_ in id_to_frags:
        if ntest_frags <= 1:
            for vector in id_to_frags[id_]:
                test_f.write(vector+'\n')
                ntest_frags -= 1
        else:
            for vector in id_to_frags[id_]:
                train_f.write(vector+'\n')
        
    test_f.close()
    train_f.close()
