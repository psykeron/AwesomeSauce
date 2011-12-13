# -*- coding: utf-8 -*-
__author__ = 'Simran Fitzgerald'

import os
from optparse import OptionParser

def fragmentFile(srcPath, trgPath, filename):
    """This function takes in a file (filename) and and breaks up the file into 512-byte blocks.  	The function will return a list containing the fragments.
    """

    #Open the file for reading
    theFile = open(os.path.join(srcPath, filename),'rb')
    
    filenameComponents = filename.split('.')
    
    if len(filenameComponents) != 2:
        return
    
    #Create the outputFile
    #output = open('outFile.out', 'ab')

    #The list that holds fragments
    #fragmentList = []
    num_fragments = 0

    #iterate through and store the 512 byte blocks in a list
    bytes = theFile.read(512)
    counter = 0
    while True:

        if bytes:
	    while len(bytes) < 512:
	        bytes += '\x00'
            #fragmentList.append(bytes)
            num_fragments += 1
	    output  = open(os.path.join(trgPath, '%s-%s.%s' % (filenameComponents[0], str(counter), filenameComponents[1])), 'ab')
            output.write(bytes)
            counter += 1
        else:

            break

        bytes = theFile.read(512)

    #close the files
    theFile.close()
    output.close()
   
    print "Number of Fragments: " + str(num_fragments)
    #print fragmentList
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input-dir", dest="input_dir", default="../data/mini",
        help="Directory containing the files to be fragmented (default ../data/001)")
    parser.add_option("-o", "--output-dir", dest="output_dir", default="fragments",
        help="Directory to write fragments to (default fragments)")
    parser.add_option("-l", "--limit", dest="limit", default=None, type=int,
	help="limit to number of files inspected")
        
    (options, args) = parser.parse_args()
    for fname in os.listdir(options.input_dir)[:options.limit]:
        fragmentFile(options.input_dir, options.output_dir, fname)
    
    
    

  
