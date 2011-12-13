import os
import sys

#Dictionary which contains file extensions as keys and number of files of that type as the value
fileDictionary = {}

#processes files into fileDictionary by directiory
def fileDict(directoryPath):


	for file in os.listdir(directoryPath):
		
		if not os.path.isfile(os.path.join(directoryPath,file)):
			continue

		extTemp = file.split('.')
		
		if len(extTemp) < 2:
			continue
		
		ext = extTemp[-1]
		#checks for a file extension
		if ext in fileDictionary:
			fileDictionary[ext] += 1
		else:
		
			fileDictionary[ext] = 1
	


if __name__ == '__main__':

	if len(sys.argv) < 2:
		exit(0)
	
	for dir in os.listdir(sys.argv[1]):
		if os.path.isdir(os.path.join(sys.argv[1],dir)):	
			fileDict(os.path.join(sys.argv[1],dir))
	
	sortedDict = sorted(fileDictionary)
	
	#Prints sorted dictionary with values
	for key in sortedDict:
		print "%s: %s" % (key, fileDictionary[key]) 

	
	temp = 0
	for v in fileDictionary.values():
		
		temp += v

		
	print 'Total number of files: ' + str(temp)
	
	
	
