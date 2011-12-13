from optparse import OptionParser
import os
from collections import defaultdict


##---------------------- Feature Calculators ----------------------------- ##

# All the below functions take as input a file fragment, as a raw string, and
# a boolean variable indicating whether to normalize results by length. They
# return a list (in many cases of length one) describing some feature of the
# file fragment.

# Many functions have no way to sensibly normalize their results, but they
# must take the second argument regardless, for consistency.

def unigram_counts(fragment, normalize=False):
    counts = defaultdict(int)
    for byte in fragment:       
        counts[byte] += 1
        
    return [ counts[chr(byte)]/(len(fragment)+0.0 if normalize else 1)
        for byte in range(255)]
    
def bigram_counts(fragment, normalize=False):
    counts = defaultdict(int)
    for i in range(len(fragment)-1):
        counts[fragment[i]+fragment[i+1]] += 1
        
    return [counts[chr(b1)+chr(b2)]/(len(fragment)+0.0 if normalize else 1)
        for b1 in range(255) for b2 in range(255)]
        
def contiguity(fragment, normalize):
    """ A vague measurement of the average contiguity from byte to byte.
    """
    total_diff = 0
    total = 0
    for i in range(len(fragment)-1):
        total_diff += abs(ord(fragment[i]) - ord(fragment[i+1]))
        total += 1
        
    return [total_diff/(total+0.0)]
    
def mean_byte_value(fragment, normalize):
    return [ sum([ord(char) for char in fragment]) / (len(fragment)+0.0) ]

def longest_streak(fragment, normalize):
    """ The length of the longest repeating subsequence. Is normalized.
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
            
    return [longest/(len(fragment)+0.0 if normalize else 1)]

## ----------------------------------------------------------------------- ##

    
def to_vectorfile_format(label, vector):
    """
    Given a label (e.g. 1, 2, 3, 4) and a list representing a vector, return a
    vector string that fits the format used by libsvm and svm-light.
    """
    vector_string = str(label)
    feat_index = 1 # Start from 1 rather than 0, oddly
    for value in vector:
        vector_string += " " + str(feat_index) + ":" + str(value)
        feat_index += 1
        
    return vector_string + '\n'

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input-dir", dest="input_dir", default="fragments",
        help="Directory containing the files to be processed (default ./fragments)")
    parser.add_option("-o", "--output-dir", dest="output_dir", default="vectors",
        help="Directory to write vector file to (default ./vectors)")
    parser.add_option("-l", "--label", dest="label", default="",
        help="String to be added to the name of the output vector file")
    parser.add_option("-n", "--norm", dest="normalize", action="store_true", default=False,
        help="Whether or not to normalize measures by the length of the fragment.")
    
    (options, args) = parser.parse_args()
    
    features = [unigram_counts, contiguity, mean_byte_value, longest_streak]#,bigram_counts]
    
    output_fname = os.path.join(options.output_dir, 'vector' + options.label + '.svm')
    out = open(output_fname, 'w')
    
    for fragment_name in os.listdir(options.input_dir):
        f = open(os.path.join(options.input_dir, fragment_name))
        fragment = f.read()
        f.close()
        
        vector = sum([feature_calc(fragment, options.normalize) for feature_calc in features], [])
        
        label = 1 if fragment_name.lower().endswith('.pdf') else -1
        vector_str = to_vectorfile_format(label, vector)
        
        out.write(vector_str)
        
    out.close()
        
        
            
        
    
    
