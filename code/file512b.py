# -*- coding: utf-8 -*-
__author__ = 'Simran Fitzgerald'

import os
from optparse import OptionParser

def fragmentFile(srcPath, trgPath, filename):
    """This function takes in a file (filename) and and breaks up the file into 512-byte blocks.
       The function will return a list containing the fragments.
    """
    
    #Open the file for reading
    theFile = open(os.path.join(srcPath, filename),'rb')
    
    filenameComponents = filename.split('.')
    
    counter = 1
    
    #iterate through and store the 512 byte blocks in a list
    bytes = theFile.read(512)
    
    # omit first fragment
    bytes = theFile.read(512)
    while bytes:
        
        # omit last fragment (if it is not 512 bytes in size)
        if len(bytes) < 512:
            break
        output = open(os.path.join(trgPath, '%s-%s.%s' % (filenameComponents[0], str(counter), filenameComponents[1])), 'ab')
        output.write(bytes)
        output.close()
        counter += 1
        bytes = theFile.read(512)
    
    #close the files
    theFile.close()
   
    print "Number of Fragments: " + (str(counter - 1))
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input-dir", dest="input_dir", default="../data/mini",
        help="Directory containing the files to be fragmented (default ../data/001)")
    parser.add_option("-o", "--output-dir", dest="output_dir", default="fragments",
        help="Directory to write fragments to (default fragments)")
    parser.add_option("-l", "--limit", dest="limit", default=None, type=int,
        help="limit to number of files inspected")
        
    (options, args) = parser.parse_args()
    
    if not os.path.isdir(options.output_dir):
        os.mkdir(options.output_dir)
    
    for fname in os.listdir(options.input_dir)[:options.limit]:
        ext = fname.split('.')[-1].strip()
        
        if not os.path.isdir(options.output_dir + "/" + ext):
            os.mkdir(options.output_dir + "/" + ext)
            
        fragmentFile(options.input_dir, options.output_dir + '/' + ext, fname)
    