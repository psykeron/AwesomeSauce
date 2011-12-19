# -*- coding: utf-8 -*-

import urllib
import re
#from vectorize import ALLOWED_EXTENSIONS
from optparse import OptionParser
import os
import random
import sys
import copy
import math

#FILE_TYPES = ALLOWED_EXTENSIONS.keys()
#FILE_TYPES = ['bmp', 'csv', 'doc', 'docx', 'eps', 'gif', 'gz', 'html', 'jar', 'java', 'jpg', 'js', 'pdf', 'png', 'pps', 'ppt', 'pptx', 'ps', 'pub', 'sql', 'swf', 'txt', 'ttf', 'xbm', 'xls', 'xlsx', 'xml', 'zip']
FILE_TYPES = ['pdf', 'html', 'jpg', 'doc', 'txt', 'xls', 'ppt', 'gif', 'xml', 'ps', 'csv', 'gz', 'png', 'swf', 'pps', 'rtf', 'sql', 'java', 'pptx', 'docx', 'tex', 'bmp', 'xlsx', 'zip',]
#FILE_TYPES = ['ttf', 'zip', 'xbm']
BASE_URL = 'https://domex.nps.edu/corp/files/govdocs1/'
#MIN_FILE_SIZE = 512 * 100
#MAX_FILE_SIZE =  512 * 500
#FILE_LIMIT = 10

regex = re.compile('\]\"></td><td><a href=\".*?\">(.*?)</a>\s*?</td><td align=\"right\">(.*?)\s*?</td><td align=\"right\">\s*?(.*?)<')

files = {}

#def size_is_in_range(size):
#    size = size.strip()
#    sizeVal = 0.0
#    if size[-1] == 'K':
#        sizeVal = float(size[0:-1]) * 1024.0
#    elif size[-1] == 'M':
#        sizeVal = float(size[0:-1]) * 1048576.0
#    elif size[-1] == 'G':
#        sizeVal = float(size[0:-1]) * 1073741824.0
#    else:
#        sizeVal = float(size)
#    return float(MIN_FILE_SIZE) < sizeVal < float(MAX_FILE_SIZE)

#def process_file(filename, size):
#    if not size_is_in_range(size):
#        return
#    extension = filename.split('.')[-1]
#    if not extension in FILE_TYPES:
#        return
#    if (not extension in files) and (FILE_LIMIT > 0):
#        files[extension] = [filename]
#    elif (0 < len(files[extension]) < FILE_LIMIT) and (files[extension].count(filename) == 0):
#        files[extension].append(filename)

#def process_page(content):
#    m = regex.search(content)
#    while m:
#        process_file(m.group(1), m.group(3))
#        content = content[m.end():]
#        m = regex.search(content)

# Download (at random) at least min_files many files that make up about target_fragments many fragments
def download_files(target_fragments=1000, min_files=10, only_allowed_file_types=True):
    files_list = []
    for file_type in sorted(files.keys()):
        if only_allowed_file_types and not file_type in FILE_TYPES:
            continue
        total_size = 0.0
        total_files = 0
        for a_file in files[file_type]:
            if a_file[1] < 1024.0:
                continue
            total_size += a_file[1]
            total_files += 1
        num_fragments = int(total_size/512.0)
        if num_fragments < target_fragments:
            continue
        if total_files < min_files:
            continue
        the_files = copy.copy(files[file_type])
        random.shuffle(the_files)
        fragments_so_far = 0
        files_to_append = []
        for a_file in the_files:
            if fragments_so_far >= target_fragments and len(files_to_append) >= min_files:
                break
            if a_file[1] < 1024.0:
                continue
            fragments_so_far += int(a_file[1]/512.0)
            files_to_append.append(a_file[0])
        files_list = files_list + files_to_append
    for filename in files_list:
        print 'Downloading %s' % os.path.join(BASE_URL, filename[0:3], filename)
        urllib.urlretrieve(os.path.join(BASE_URL, filename[0:3], filename), os.path.join(options.output_dir, filename))
    print 'Downloaded %i files' % len(files_list)
    return

def data_on_files(min_fragments=0, max_fragments=sys.maxint, only_allowed_file_types=False):
    print 'File type\t# files\t\t# fragments'
    for file_type in sorted(files.keys()):
        if only_allowed_file_types and not file_type in FILE_TYPES:
            continue
        total_size = 0.0
        total_files = 0
        for a_file in files[file_type]:
            if a_file[1] < 1024.0:
                continue
            total_size += a_file[1]
            total_files += 1
        num_fragments = int(total_size/512.0)
        if num_fragments < min_fragments:
            continue
        print '%s\t\t%i\t\t%i' % (file_type, total_files, num_fragments)

def total_fragments_for_each_file_type():
    print 'File type\t# files\t\t# fragments'
    for file_type in sorted(files.keys()):
        total_fragments = 0.0
        total_files = 0
        for a_file in files[file_type]:
            total_fragments += int(math.ceil(a_file[1]/512.0))
            total_files += 1
        print '%s\t\t%i\t\t%i' % (file_type, total_files, total_fragments)

def get_file_size(size):
    size = size.strip()
    if size[-1] == 'K':
        return float(size[0:-1]) * 1024.0
    elif size[-1] == 'M':
        return float(size[0:-1]) * 1048576.0
    elif size[-1] == 'G':
        return float(size[0:-1]) * 1073741824.0
    else:
        return float(size)

def process_files_list():
    files_list_file = open(options.files_list, 'r')
    line = files_list_file.readline()
    while line:
        line = line.strip()
        file_name = line.split(',')[0]
        file_type = file_name.split('.')[1]
        file_size = float(line.split(',')[1])
        if not file_type in files:
            files[file_type] = [[file_name, file_size]]
        else:
            files[file_type].append([file_name, file_size])
        line = files_list_file.readline()
    files_list_file.close()
    return

def get_files_list():
    if not os.path.isfile(options.files_list):
        print 'File containing list of govdocs1 files was not found. Creating...'
        files_list_file = open(options.files_list, 'a')
        for i in range(1000):
            print 'Looking for files in %s' % (BASE_URL + '%.3i' % i)
            content = urllib.urlopen(BASE_URL + '%.3i' % i).read()
            m = regex.search(content)
            while m:
                files_list_file.write('%s,%f\n' % (m.group(1), get_file_size(m.group(3))))
                content = content[m.end():]
                m = regex.search(content)
        files_list_file.close()
    process_files_list()
    return
        
    

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-o', '--output-dir', dest='output_dir', default='training_data',
        help='Output directory for data files [default: ./training_data]')
    parser.add_option('-l', '--file-limit', dest='file_limit', type='int', default=10,
        help='Limit for number of files of each file type to download')
    parser.add_option('-f', '--files-list', dest='files_list', default='files_list.txt',
        help='File to store list of all files in the govdocs1 data set [default: files_list.txt]')
    
    (options, args) = parser.parse_args()
    
    FILE_LIMIT = options.file_limit
    
    get_files_list()
    
    #total_fragments_for_each_file_type()
    #exit(0)
    
    #data_on_files(min_fragments=0, only_allowed_file_types=False)
    data_on_files(min_fragments=10000, only_allowed_file_types=True)
    
    if not os.path.isdir(options.output_dir):
        os.mkdir(options.output_dir)
    
    download_files(target_fragments=10000, min_files=10, only_allowed_file_types=True)
    
#    for key in files.keys():
#        for filename in files[key]:
#            print 'Downloading %s' % os.path.join(BASE_URL, filename[0:3], filename)
#            urllib.urlretrieve(os.path.join(BASE_URL, filename[0:3], filename), os.path.join(options.output_dir, filename))
    
#    for key in files.keys():
#        print 'Downloaded %i files of type %s' % (len(files[key]), key)
