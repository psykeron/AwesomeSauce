## -*- coding: utf-8 -*-

import os
import sys
import random
import shutil
from optparse import OptionParser

#FILE_TYPES = ALLOWED_EXTENSIONS.keys()
FILE_TYPES = ['bmp', 'csv', 'doc', 'docx', 'eps', 'gif', 'gz', 'html', 'jar', 'java', 'jpg', 'js', 'pdf', 'png', 'pps', 'ppt', 'pptx', 'ps', 'pub', 'sql', 'swf', 'txt', 'ttf', 'xbm', 'xls', 'xlsx', 'xml', 'zip']

FRAGMENT_LIMIT = 100

fragment_files = {}

def process_file(filename):
    if not os.path.isfile(os.path.join(options.input_dir, filename)):
        return
    filename_components = filename.split('.')
    if len(filename_components) != 2:
        return
    file_type = filename_components[1]
    if not file_type in FILE_TYPES:
        return
    base_filename = filename_components[0].split('-')[0]
    #fragment_number = filename_components[0].split('-')[1]
    if not file_type in fragment_files:
        fragment_files[file_type] = { base_filename: [filename] }
    elif not base_filename in fragment_files[file_type]:
        fragment_files[file_type][base_filename] = [filename]
    else:
        fragment_files[file_type][base_filename].append(filename)
    return

def build_random_fragments_list():
    for file_type in fragment_files.keys():
        least_fragments = sys.maxint
        fragments = []
        for base_filename in fragment_files[file_type].keys():
            if len(fragment_files[file_type][base_filename]) < least_fragments:
                least_fragments = len(fragment_files[file_type][base_filename])
        for base_filename in fragment_files[file_type].keys():
            random.shuffle(fragment_files[file_type][base_filename])
            fragments = fragments + fragment_files[file_type][base_filename][0:least_fragments]
        random.shuffle(fragments)
        fragment_files[file_type] = fragments[0:FRAGMENT_LIMIT]

def output_fragments():
    for file_type in fragment_files.keys():
        for filename in fragment_files[file_type]:
            print 'Copying %s to %s' % (os.path.join(options.input_dir, filename), os.path.join(options.output_dir, filename))
            shutil.copy(os.path.join(options.input_dir, filename), os.path.join(options.output_dir, filename))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input-dir", dest="input_dir", default="fragments",
        help="Directory containing the file fragments [default: ./fragments]")
    parser.add_option("-o", "--output-dir", dest="output_dir", default="random_fragments",
        help="Directory to output subset of file fragments to [default: ./random_fragments)")
    parser.add_option("-l", "--fragment-limit", dest="fragment_limit", default=100, type=int,
        help="Limit for the number of file fragments of each file type to output [default: 100]")
    
    (options, args) = parser.parse_args()
    
    FRAGMENT_LIMIT = options.fragment_limit
    
    if not os.path.isdir(options.input_dir):
        print "Directory \"" + options.input_dir + "\" does not exist"
        exit(1)
    
    if not os.path.isdir(options.output_dir):
        os.mkdir(options.output_dir)
    
    for filename in os.listdir(options.input_dir):
        process_file(filename)
    
    build_random_fragments_list()
    output_fragments()
    