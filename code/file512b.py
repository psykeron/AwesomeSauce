# -*- coding: utf-8 -*-
__author__ = 'Simran Fitzgerald'

import os

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
    fragmentList = []

    #iterate through and store the 512 byte blocks in a list
    bytes = theFile.read(512)
    counter = 0
    while True:

        if bytes:
	    while len(bytes) < 512:
	        bytes += '\x00'
            fragmentList.append(bytes)
	    output  = open(os.path.join(trgPath, '%s-%s.%s' % (filenameComponents[0], str(counter), filenameComponents[1])), 'ab')
            output.write(bytes)
	    counter += 1
        else:

            break

        bytes = theFile.read(512)

    #close the files
    theFile.close()
    output.close()
   
    print "Number of Fragments: " + str(len(fragmentList))
    #print fragmentList
    

  
