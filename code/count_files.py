# -*- coding: utf-8 -*-

import os
import sys

files = {}

if __name__ == '__main__':
    for file in os.listdir(sys.argv[1]):
        extension = file.split('.')[-1]
        if not extension in files:
            files[extension] = [file]
        else:
            files[extension].append(file)
    
    for key in files.keys():
        print 'There are %i files of type %s' % (len(files[key]), key)
    