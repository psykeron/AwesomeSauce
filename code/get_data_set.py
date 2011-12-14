# -*- coding: utf-8 -*-

import urllib
import re
from vectorize import ALLOWED_EXTENSIONS
from optparse import OptionParser
import os

FILE_TYPES = ALLOWED_EXTENSIONS.keys()
BASE_URL = 'https://domex.nps.edu/corp/files/govdocs1/'
MIN_FILE_SIZE = 512 * 10
MAX_FILE_SIZE = 512 * 1000
FILE_LIMIT = 10

regex = re.compile('\]\"></td><td><a href=\".*?\">(.*?)</a>\s*?</td><td align=\"right\">(.*?)\s*?</td><td align=\"right\">\s*?(.*?)<')

files = {}

def size_is_in_range(size):
    size = size.strip()
    sizeVal = 0.0
    if size[-1] == 'K':
        sizeVal = float(size[0:-1]) * 1024.0
    elif size[-1] == 'M':
        sizeVal = float(size[0:-1]) * 1048576.0
    elif size[-1] == 'G':
        sizeVal = float(size[0:-1]) * 1073741824.0
    else:
        sizeVal = float(size)
    return float(MIN_FILE_SIZE) < sizeVal < float(MAX_FILE_SIZE)

def process_file(filename, size):
    if not size_is_in_range(size):
        return
    extension = filename.split('.')[-1]
    if not extension in FILE_TYPES:
        return
    if (not extension in files) and (FILE_LIMIT > 0):
        files[extension] = [filename]
    elif (0 < len(files[extension]) < FILE_LIMIT) and (files[extension].count(filename) == 0):
        files[extension].append(filename)

def process_page(content):
    m = regex.search(content)
    while m:
        process_file(m.group(1), m.group(3))
        content = content[m.end():]
        m = regex.search(content)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-o', '--output-dir', dest='output_dir', default='training_data',
        help='Output directory for data files [default: ./training_data]')
    parser.add_option('-l', '--file-limit', dest='file_limit', type='int', default=10,
        help='Limit for number of files of each file type to download')
    
    (options, args) = parser.parse_args()
    
    FILE_LIMIT = options.file_limit
    
    for i in range(1000):
        print 'Looking for files in %s' % (BASE_URL + '%.3i' % i)
        process_page(urllib.urlopen(BASE_URL + '%.3i' % i).read())
    
    if not os.path.isdir(options.output_dir):
        os.mkdir(options.output_dir)
    
    for key in files.keys():
        for filename in files[key]:
            print 'Downloading %s' % os.path.join(BASE_URL, filename[0:3], filename)
            urllib.urlretrieve(os.path.join(BASE_URL, filename[0:3], filename), os.path.join(options.output_dir, filename))

