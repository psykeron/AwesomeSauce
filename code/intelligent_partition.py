# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
from collections import defaultdict

def build_offset_list(filename):
    """This fuction will return a list of line offsets for the given file with name 'filename'.  
    Once one has the list, it can be used to seek to a particular line in the file where in the index of the list is the line one
    wishes to reference
    """
    the_file = open(filename)
    line_offset = []
    offset = 0
    for line in the_file:
	line_offset.append(offset)
	offset += len(line)
	
    the_file.close()
    
    return line_offset

  

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
    id_to_nfrags = defaultdict(int)

    for line in f:
        frag_id = line.split('#')[1].strip()
        id_to_nfrags[frag_id] += 1
    
    #remember to close that shit!	
    #f.close()
    
    total_frags = sum(id_to_nfrags.values() )
    ntest_frags = int(options.test_data_ratio*total_frags)
    
    test_ids = set([])
    for id_ in id_to_nfrags:
        test_ids.add(id_)
        ntest_frags -= id_to_nfrags[id_]
        if ntest_frags <= 0:
            break
            
    print "Picked %d files to use in test file" % (len(test_ids))
    
    test_f = open(options.test_fname, 'w')
    train_f = open(options.train_fname, 'w')
    
    f.seek(0)
    for line in f:
        frag_id = line.split('#')[1].strip()
        if frag_id in test_ids:
            test_f.write(line)
        else:
            train_f.write(line)
    
        
    #close files!    
    test_f.close()
    train_f.close()
