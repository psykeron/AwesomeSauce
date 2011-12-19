#!/usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os
from collections import defaultdict
import bz2
import random
import math
from get_data_set import FILE_TYPES

#FILE_TYPES = ['bmp', 'csv', 'doc', 'docx', 'eps', 'gif', 'gz', 'html', 'jar', 'java', 'jpg', 'js', 'pdf', 'png', 'pps', 'ppt', 'pptx', 'ps', 'pub', 'sql', 'swf', 'txt', 'ttf', 'xbm', 'xls', 'xlsx', 'xml', 'zip']

ALLOWED_EXTENSIONS = dict([ (ext, num) for (ext, num) in zip(FILE_TYPES, range(1,len(FILE_TYPES)+1))])

# Arbitrary mapping from extensions we're interested in to numerical labels
#ALLOWED_EXTENSIONS = {'html':1, 'txt':2, 'gif':3, 'jpg':4, 'ppt':5, 'doc':6, 'pdf':7, 
#    'gz':8, 'doc':9, 'png':10, 'xml':11, 'xls':12}


##---------------------- Feature Calculators ----------------------------- ##

# All the below functions take as input a file fragment, as a raw string. They
# return a list (in many cases of length one) describing some feature of the
# file fragment.

def unigram_counts(fragment):
    counts = defaultdict(int)
    for byte in fragment:       
        counts[byte] += 1
        
    return [ counts[chr(byte)] for byte in range(255) ]
    
def entropy_and_bigram_counts(fragment):
    """Package together to avoid having to calculate this a second time when
    calculating entropy.
    """
    counts = defaultdict(int)
    for i in range(len(fragment)-1):
        counts[fragment[i]+fragment[i+1]] += 1
        
    bigram_frequencies = [counts[chr(b1)+chr(b2)] for b1 in range(255) for b2 in range(255)]
    
    entropy = 0.0
    #bigram_frequencies = bigram_counts(fragment)
    for i in range(len(bigram_frequencies)):
        if bigram_frequencies[i] > 0.0:
            entropy += bigram_frequencies[i] * math.log10(bigram_frequencies[i])
    entropy = -entropy
    
    #return [entropy]
    
    return [entropy] + bigram_frequencies
        
def contiguity(fragment):
    """ A vague measurement of the average contiguity from byte to byte.
    """
    total_diff = 0
    total = 0
    for i in range(len(fragment)-1):
        total_diff += abs(ord(fragment[i]) - ord(fragment[i+1]))
        total += 1
        
    return [total_diff/(total+0.0)]

def mean_byte_value(fragment):
    return [ sum([ord(char) for char in fragment]) ]

def longest_streak(fragment):
    """ The length of the longest repeating subsequence.
    """
    longest = 0
    last = fragment[0]
    current_streak = 1
    for char in fragment[1:]:
        if char == last:
            current_streak += 1
        else:
            if current_streak > longest:
                longest = current_streak
            last = char
            current_streak = 1
            
    return [longest]
    
def compressed_length(fragment):
    """Return a feature vector with the ratio of the compressed length of the
    file fragment to the actual length of the file fragment
    """
    return [ float( len(bz2.compress(fragment)) ) / float(len(fragment)) ]
    
def entropy(fragment):
    entropy = 0.0
    bigram_frequencies = bigram_counts(fragment)
    for i in range(len(bigram_frequencies)):
        if bigram_frequencies[i] > 0.0:
            entropy += bigram_frequencies[i] * math.log10(bigram_frequencies[i])
    entropy = -entropy
    
    return [entropy]
    
def chi_squared(fragment):
    chi_squared = 0.0
    C2 = 0.0
    expected = 2.0 #expected frequency of a byte (fileSize/number of possible byte values)->(512/256)
    
    for index in range(0,256):
        observed = feature_vector_1grams[index]
        C2 += ((observed-expected)**2)/expected
    
    chi_squared = stats.achisqprob(C2,255)
    
    return [chi_squared]
    
def hamming_weight(fragment):
    hamming_weight = 0.0
    for i in range(len(fragment)):
        current_byte = ord(fragment[i])
    while current_byte != 0:
        hamming_weight += float(current_byte & 1)
        current_byte = current_byte >> 1
    hamming_weight /= float(8 * len(fragment))
    
    return [hamming_weight]

## ----------------------------------------------------------------------- ##

    
def to_vectorfile_format(label, vector):
    """
    Given a label (e.g. 1, 2, 3, 4) and a list representing a vector, return a
    vector string that fits the format used by libsvm and svm-light.
    """
    vector_string = str(label)
    feat_index = 1 # Start from 1 rather than 0, oddly
    for value in vector:
        # Can save a ton of space by ignoring 0-valued features
        if value != 0:
            vector_string += " " + str(feat_index) + ":" + str(value)
        feat_index += 1
        
    return vector_string

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input-dir", dest="input_dir", default="fragments",
        help="Directory containing the files to be processed (default ./fragments)")
    parser.add_option("-o", "--output-dir", dest="output_dir", default="/h/90/oles/csc2208h/vectors",
        help="Directory to write vector file to (default ./vectors)")
    parser.add_option("-l", "--label", dest="label", default="",
        help="String to be added to the name of the output vector file")
    parser.add_option("-n", "--limit", dest="limit", type=int, default=0,
        help="Limit to the number of fragments to take of each type. Default: 0=unlimited.")
    
    (options, args) = parser.parse_args()
    
    features = [unigram_counts, contiguity, mean_byte_value, longest_streak, compressed_length, hamming_weight, entropy_and_bigram_counts]
    
    output_fname = os.path.join(options.output_dir, 'vector' + options.label + '.svm')
    out = open(output_fname, 'w')
    
    fragments_seen = 0
    
    #for fragment_name in os.listdir(options.input_dir):
    #for (dirpath, dirnames, fnames) in os.walk(options.input_dir):
    for subdir in os.listdir(options.input_dir):
        fulldir = os.path.join(options.input_dir, subdir)
        frags = os.listdir(fulldir)
        # If we're only taking a subset of the fragments (when options.limit is set), we want to make sure it's a random one
        random.shuffle(frags)
        for fragment_name in (frags[:options.limit] if options.limit else frags):
            fragments_seen += 1
            if (fragments_seen % 1000) == 0:
                print "On %dth fragment" % (fragments_seen)
            f = open(os.path.join(fulldir, fragment_name))
            fragment = f.read()
            f.close()
            
            ext = fragment_name.lower().split('.')[-1]
            if ext not in ALLOWED_EXTENSIONS:
                continue
            
            vector = sum([feature_calc(fragment) for feature_calc in features], [])
            
            # 352352-3.jpg
            frag_identifier = fragment_name.split('-')[0]
            
            vector_str = to_vectorfile_format(ALLOWED_EXTENSIONS[ext], vector) + "#" + frag_identifier + "\n"
            
            out.write(vector_str)
        
    out.close()
        
        
            
        
    
    
