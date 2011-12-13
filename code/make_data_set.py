# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import shutil
import sys
from vectorize import ALLOWED_EXTENSIONS

FILE_TYPES = ALLOWED_EXTENSIONS.keys()

filenames = {}

def process_file(dir, filename):
    if not os.path.isfile(os.path.join(options.input_dir, dir, filename)):
        return
    file_type = filename.split('.')[-1]
    if not file_type in FILE_TYPES:
        return
    if (not file_type in filenames) and (options.file_limit > 0):
        filenames[file_type] = [os.path.join(dir, filename)]
        return
    if 0 < len(filenames[file_type]) < int(options.file_limit) and filenames[file_type].count(os.path.join(dir, filename)) == 0:
        filenames[file_type].append(os.path.join(dir, filename))
        return


def output_data_set():
    for type in filenames.keys():
        for filepath in filenames[type]:
            print "copying", os.path.join(options.input_dir, filepath), "to", os.path.join(options.output_dir, os.path.split(filepath)[1])
            shutil.copy(os.path.join(options.input_dir, filepath), os.path.join(options.output_dir, os.path.split(filepath)[1]))





if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input-dir", dest="input_dir", default="/h/90/oles/csc2208h/data",
        help="Directory containing the raw Garfinkel data set (default: /h/90/oles/csc2208h/data)")
    parser.add_option("-o", "--output-dir", dest="output_dir", default="training_data",
        help="Directory to write our data set to (default: ./training_data)")
    parser.add_option("-l", "--file-limit", dest="file_limit", default="10",
        help="Limit for total number of each file type to output")
    
    (options, args) = parser.parse_args()
    
    if not os.path.isdir(options.input_dir):
        print "Directory \"" + options.input_dir + "\" does not exist"
        exit(1)
    
    if not os.path.isdir(options.output_dir):
        os.mkdir(options.output_dir)
    
    #print FILE_TYPES
    
    for dir in os.listdir(options.input_dir):
        if os.path.isdir(os.path.join(options.input_dir, dir)):
            for file in os.listdir(os.path.join(options.input_dir, dir)):
                process_file(dir, file)
    
    output_data_set()
