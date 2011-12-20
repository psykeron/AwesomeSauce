#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
from collections import defaultdict
from get_data_set import FILE_TYPES
import random

LABEL_LOOKUP = dict([ (num, ext) for (ext, num) in zip(FILE_TYPES, range(1,len(FILE_TYPES)+1))])

# This quantifies how high we want to set the minimum fragments per class. A higher value will increase the minimum, but cause the actual ratio of training to testing data to be off. 
# E.g. If there are 1000 fragments spread over 10 classes, and our ratio is 1.0, we will want a total of 100 fragments for
# our test set. If DISPARITY_INTOLERANCE is set to 1.0, then each class will require a minimum of 10 fragments. Because
# we either take all the fragments in a file or none at all, the actual number of test fragments will certainly exceed 100.
# If DISPARITY_INTOLERANCE is set to 0.5, then each class will only need a minimum of 5 fragments.

DISPARITY_INTOLERANCE = 0.6

CEILING = 3.0

class Fiel(object):
    
    def __init__(self, fid, label):
        self.fid = fid
        self.label = label
        
    def __hash__(self):
        # We can assume that fids are unique; that is, there are no two files with the same fid and different labels
        return hash(self.fid)
        
    def __eq__(self, other):
        return isinstance(other, Fiel) and self.fid == other.fid

  

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
    
    # Mapping of Fiel objects to number of fragments
    id_to_nfrags = defaultdict(int)

    for line in f:
        label = line.split()[0]
        file_id = line.split('#')[1].strip()
        this_fiel = Fiel(file_id, label)
        id_to_nfrags[this_fiel] += 1
    
    total_frags = sum(id_to_nfrags.values() )
    ntest_frags = int(options.test_data_ratio*total_frags)
    ntest_frags_orig = ntest_frags
                                                          
    
    nclasses = len(FILE_TYPES)
    min_frags_per_class = int(ntest_frags/(nclasses+0.0) * DISPARITY_INTOLERANCE)
    # A dict mapping classes to the number of fragments required for that class
    class_to_reqfrags = dict( (str(classlabel), min_frags_per_class) for classlabel in range(1, len(FILE_TYPES)+1) )
    
    print "Found %d total fragments over %d files. Aiming to use %d fragments for test data, with minimum %d per class" % (total_frags, len(id_to_nfrags), ntest_frags, min_frags_per_class)
    
    test_ids = set([])
    # Step one: attain the minimum for each class
    for fiel in id_to_nfrags:
        if class_to_reqfrags[fiel.label] > 0:
            if id_to_nfrags[fiel] + (min_frags_per_class-class_to_reqfrags[fiel.label]) > (min_frags_per_class*CEILING):
                print "Skipping file to avoid going above ceiling"
            else:
                test_ids.add(fiel.fid)
                class_to_reqfrags[fiel.label] -= id_to_nfrags[fiel]
                ntest_frags -= id_to_nfrags[fiel]
            
    print "After attaining minimum per each class with %d files, we have %d fragments left to fill" % (len(test_ids), ntest_frags)
        
    bugged = False
    for label in range(1, len(FILE_TYPES)+1):
        if class_to_reqfrags[str(label)] > 0 and label != 16:
            print "Class %s still needs %d more fragments allocated" % (LABEL_LOOKUP[label], class_to_reqfrags[str(label)])
            bugged = True
    if bugged:
        raise Exception("I done wrong.")
    #assert not any([ (class_to_reqfrags[str(label)] > 0) for label in range(1, len(FILE_TYPES)+1) ]), "There were some file types that didn't get the minimum number of fragments, for some reason"
    
    fiels = id_to_nfrags.keys()
    fiels = set(fiels)
    fiels.difference_update(test_ids) # Have to make sure we don't double-add files
    fiels = list(fiels)
    random.shuffle(fiels)
    
    for fiel in fiels:
        if ntest_frags <= 0:
            break
        if id_to_nfrags[fiel] + (min_frags_per_class-class_to_reqfrags[fiel.label]) > (min_frags_per_class*CEILING):
            print "Skipping file to avoid going above ceiling"
        else:
            test_ids.add(fiel.fid)
            ntest_frags -= id_to_nfrags[fiel]
            class_to_reqfrags[fiel.label] -= id_to_nfrags[fiel]
    else:
        print "WARNING: exhausted file list before getting the required number of test fragments"
            
    print "Picked %d files to use in test file" % (len(test_ids))
    actual_test_frags = ntest_frags_orig - ntest_frags
    actual_ratio = actual_test_frags / (total_frags + 0.0)
    print "Selected %d test fragments leading to an actual test:train ratio of %.2f" % (actual_test_frags, actual_ratio)
    
    test_f = open(options.test_fname, 'w')
    train_f = open(options.train_fname, 'w')
    
    f.seek(0)
    for line in f:
        #label = line.split()[0]
        frag_id = line.split('#')[1].strip()
        if frag_id in test_ids:
            test_f.write(line)
        else:
            train_f.write(line)
    
        
    #close files!    
    test_f.close()
    train_f.close()
