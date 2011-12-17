# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
from collections import defaultdict

def build_offset_list(filename):
    """This fuction will return a list of line offsets for the given file with name 'filename'.  
    Once one has the list, it can be used to seek to a particular line in the file where in the index of the list is the line one
    wishes to reference
    """
    the_file = open(filename)
    line_offset = []
    offset = 0
    for line in the_file:
	line_offset.append(offset)
	offset += len(line)
	
    the_file.close()
    
    return line_offset

  

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-r', '--test-data-ratio', dest='test_data_ratio', type=float, default=0.1,
        help='Ratio of data to be used for testing [default: 0.1]')
    parser.add_option('--train-fname', dest='train_fname', default='train.svm',
        help='Filename to save training vectors to')
    parser.add_option('--test-fname', dest='test_fname', default='test.svm',
        help='Filename to save testing vectors to')


    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        print 'Usage: %s [-r <ratio>] <vectors-filename>' % sys.argv[0]
        sys.exit(1)
    
    fname = args[0]
    
    f = open(fname, 'r')
    
    # Mapping of file id to vectors
    id_to_frags = defaultdict(list)

    # Note from Colin: Probably the reason this loop is causing OoM is that it requires putting the whole vector into memory. Fix idea: map, fragment ids to indices in the vector file, rather than a list of actual vectors. Then decide which ids are testing and training. Then iterate through vector file again, selectively copying to either the training or testing file.
    
    #this try-except block is to help us see when the 'Memory Error' is occuring with respect to how many lines are read
    input_file_index=0
    try:
      for line in f:
	  
	  if (input_file_index % 1000) == 0:
	      
	      print "Currently on line " + str(input_file_index) + " of input file."
	  
	  #mapping frag ids to index in input vector file (as per colin's fix idea from above)
	  frag_id = line.split('#')[1].strip()
	  id_to_frags[frag_id].append(input_file_index)
	  input_file_index += 1
	  
    except Exception as e:
      print e
	
    #remember to close that shit!	
    f.close()
    
    total_frags = sum([len(id_to_frags[id_]) for id_ in id_to_frags] )
    ntest_frags = int(options.test_data_ratio*total_frags)
    
    test_f = open(options.test_fname, 'w')
    train_f = open(options.train_fname, 'w')
    
    #build line offset list!
    line_offset_list  = build_offset_list(fname)
    
    #open original input vector file again
    f2 = open(fname)
    
    #write to output--train and test svm files
    for id_ in id_to_frags:
        if ntest_frags <= 1:
            for vector_index in id_to_frags[id_]:
		#using the line_offset_list, we can f2.seek(byte) by line!
		f2.seek(line_offset_list[vector_index])
		
                test_f.write(f2.readline())# +'\n') -- I don't think we need this...?
                ntest_frags -= 1
        else:
            for vector_index in id_to_frags[id_]:
		f2.seek(line_offset_list[vector_index])
                train_f.write(f2.readline())#+'\n') -- I dont think we need this...?
        
    #close files!    
    test_f.close()
    train_f.close()
    f2.close()
