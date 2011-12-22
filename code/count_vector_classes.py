#!/usr/bin/python
# -*- coding: utf-8 -*-

from get_data_set import FILE_TYPES
from optparse import OptionParser
from collections import defaultdict
import sys

LABEL_LOOKUP = dict([ (num, ext) for (ext, num) in zip(FILE_TYPES, range(1,len(FILE_TYPES)+1))])

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--predictions", dest="predictions", default="output.svm",
        help="File containing the SVM's predictions (default: output.svm)")
    parser.add_option("-t", "--true", dest="true", default="test.svm",
        help="File of test vectors, containing the true labels (default: test.svm)")
    parser.add_option("-d", "--delim", dest="delim", default="\t",
        help="String to use as delimiter for tabular output (default:tab)")
       
    
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        print "Usage: count_vector_classes.py blah.svm"
        sys.exit(1)
        
    f = open(args[0])
    class_to_count = defaultdict(int)
    for line in f:
        label = line.split()[0]
        class_to_count[label] += 1
        
    f.close()
    for classno in class_to_count:
        print "%s: %d" % (LABEL_LOOKUP[int(classno)], class_to_count[classno])