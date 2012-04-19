#! /usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os
from get_data_set import FILE_TYPES





def micro_averaged_F_measure(preds, trues):
    true_pos = dict(zip(range(1,len(FILE_TYPES)+1),[0]*len(FILE_TYPES)))
    false_pos = dict(zip(range(1,len(FILE_TYPES)+1),[0]*len(FILE_TYPES)))
    false_neg = dict(zip(range(1,len(FILE_TYPES)+1),[0]*len(FILE_TYPES)))
    for i in range(len(trues)):
        if trues[i] == preds[i]:
            true_pos[trues[i]] += 1
        else:
            false_pos[preds[i]] += 1
            false_neg[trues[i]] += 1
    precision_num = 0.0
    precision_denom = 0.0
    recall_num = 0.0
    recall_denom = 0.0
    for file_type in range(1,len(FILE_TYPES)+1):
        precision_num += float(true_pos[file_type])
        precision_denom += (float(true_pos[file_type]) + float(false_pos[file_type]))
        recall_num += float(true_pos[file_type])
        recall_denom += (float(true_pos[file_type]) + float(false_neg[file_type]))
    precision = precision_num / precision_denom
    recall = recall_num / recall_denom
    return (2.0 * precision * recall)/(precision + recall)

def macro_averaged_F_measure(preds, trues):    
    true_pos = dict(zip(range(1,len(FILE_TYPES)+1),[0]*len(FILE_TYPES)))
    false_pos = dict(zip(range(1,len(FILE_TYPES)+1),[0]*len(FILE_TYPES)))
    false_neg = dict(zip(range(1,len(FILE_TYPES)+1),[0]*len(FILE_TYPES)))
    for i in range(len(trues)):
        if trues[i] == preds[i]:
            true_pos[trues[i]] += 1
        else:
            false_pos[preds[i]] += 1
            false_neg[trues[i]] += 1
    precision = {}
    recall = {}
    result = 0.0
    for file_type in range(1,len(FILE_TYPES)+1):
        precision[file_type] = float(true_pos[file_type])/(float(true_pos[file_type]) + float(false_pos[file_type]))
        recall[file_type] = float(true_pos[file_type])/(float(true_pos[file_type]) + float(false_neg[file_type]))
        #print "%d: %f %f" % (file_type, precision[file_type], recall[file_type])
        result += (2.0 * precision[file_type] * recall[file_type])/(precision[file_type] + recall[file_type])
    return result / float(len(FILE_TYPES))
    
    

if __name__ == "__main__":
    parser = OptionParser()
    
    parser.add_option("-d", "--dir", dest="dir", help="Directory containing the results of one run of an experiment")
    
    (options, args) = parser.parse_args()
    
    f_pred = open(os.path.join(options.dir, "output.svm"))
    preds = [int(file_type) for file_type in f_pred.readlines()]
    f_pred.close()
    
    f_true = open(os.path.join(options.dir, "test.svm"))
    trues = [int(feature_vector.split()[0]) for feature_vector in f_true.readlines()]
    f_true.close()
    
    assert len(preds) == len(trues), "Should have same number of lines in test data as in the SVM output. Got %d and %d" % (len(preds), len(trues))
    
    print macro_averaged_F_measure(preds, trues)
    #print micro_averaged_F_measure(preds, trues)
    