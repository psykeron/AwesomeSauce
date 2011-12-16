# -*- coding: utf-8 -*-

from collections import defaultdict
from get_data_set import FILE_TYPES
from optparse import OptionParser

LABEL_LOOKUP = dict([ (num, ext) for (ext, num) in zip(FILE_TYPES, range(1,len(FILE_TYPES)+1))])

def conf_matrix_str(conf, delim="\t"):
    """Given a doubly-indexed dict from integer labels to integer labels to integer counts,
    return a tabular string representation using the given delimiter.
    
    PROTIP: Set delim=',' to get a csv file
    """
    strrep = ''
    labels = ['X'] + [LABEL_LOOKUP[lab] for lab in conf.keys()]
    strrep += delim.join(labels) + '\n'
    for l1 in conf:
        strrep += LABEL_LOOKUP[l1] + delim
        for l2 in conf:
            strrep += str(conf[l1][l2]) + delim
        strrep += '\n'
        
    return strrep
    


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--predictions", dest="predictions", default="output.svm",
        help="File containing the SVM's predictions")
    parser.add_option("-t", "--true", dest="true", default="test.svm",
        help="File of test vectors, containing the true labels")
    parser.add_option("-d", "--delim", dest="delim", default="\t",
        help="String to use as delimiter for tabular output")
       
    
    (options, args) = parser.parse_args()
    
    
    f_pred = open(options.predictions)
    preds = [int(lab) for lab in f_pred.readlines()]
    f_pred.close()
    
    f_true = open(options.true)
    trues = [int(vector.split()[0]) for vector in f_true.readlines()]
    f_true.close()
    
    assert len(preds) == len(trues), "Should have same number of lines in test data as in the SVM output. Got %d and %d" % (len(preds), len(trues))
    
    conf = defaultdict(lambda: defaultdict(int))
    
    for (true, predicted) in zip(trues, preds):
        conf[true][predicted] += 1
        
    print conf_matrix_str(conf, options.delim)
        
    