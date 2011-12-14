# -*- coding: utf-8 -*-
import bz2
import math
import stats

# return 1-grams feature vector from file fragment string
def fileFragmetToFeatureVector1Grams(fileFragment):
    feature_vector_1grams = []
    
    for i in range(0, 256):
	feature_vector_1grams.append(0.0)
	
    for i in range(0, len(fileFragment)):
	feature_vector_1grams[ord(fileFragment[i])] += 1.0
	
    for i in range(0, 256):
	feature_vector_1grams[i] = float(feature_vector_1grams[i]) / float(len(fileFragment))
    
    return feature_vector_1grams

# return 2-grams feature vector from file fragment string
def fileFragmetToFeatureVector2Grams(fileFragment):
    feature_vector_2grams = []
    
    for i in range(0, 65536):
	feature_vector_2grams.append(0.0)
	
    for i in range(0, len(fileFragment) - 1):
	feature_vector_2grams[(ord(fileFragment[i]) << 8) | ord(fileFragment[i+1])] += 1.0
	    
    for i in range(0, 65536):
	feature_vector_2grams[i] = float(feature_vector_2grams[i]) / float(len(fileFragment) - 1)
	
    return feature_vector_2grams

# returns a feature vector with the ratio of the compressed length of the file fragment to the actual length of the file fragment
def fileFragmetToFeatureVectorCompressedLength(fileFragment):
    return [float(len(bz2.compress(fileFragment))) / float(len(fileFragment))]

# returns the feature vector used in the Conti paper [entropy, arithmetic mean, chi square, Hamming weight]
def fileFragmentToFeatureVectorConti(fileFragment):
    
    #Entropy
    entropy = 0.0
    bigram_frequencies = fileFragmetToFeatureVector2Grams(fileFragment)
    for i in range(len(bigram_frequencies)):
	if bigram_frequencies[i] > 0.0:
	    entropy += bigram_frequencies[i] * math.log10(bigram_frequencies[i])
    entropy = -entropy
    
    #Arithmetic Mean
    arithmetic_mean = 0.0
    unigram_frequencies = fileFragmetToFeatureVector1Grams(fileFragment)
    for i in range(len(unigram_frequencies)):
	arithmetic_mean += float(i) * float(unigram_frequencies[i])
    
    #Chi-Squared
    chi_squared = 0.0
    C2 = 0.0
    expected = 2.0 #expected frequency of a byte (fileSize/number of possible byte values)->(512/256)
    
    for index in range(0,256):
      observed = feature_vector_1grams[index]
      C2 += ((observed-expected)**2)/expected
    
    chi_squared = stats.achisqprob(C2,255)
    
    
    
    #Hamming-Weight
    hamming_weight = 0.0
    for i in range(len(fileFragment)):
	current_byte = ord(fileFragment[i])
	while current_byte != 0:
	    hamming_weight += float(current_byte & 1)
	    current_byte = current_byte >> 1
    hamming_weight /= float(8 * len(fileFragment))

    return [entropy, arithmetic_mean, chi_squared, hamming_weight]

# 512 byte file fragment as string is passed in and the corresponding feature vector is outputtted
def fileFragmentToFeatureVector(fileFragment):
#    if len(fileFragment) != 512:
#	return None
    
    retVal = {}
    
    retVal["1grams"] = fileFragmetToFeatureVector1Grams(fileFragment)
    retVal["2grams"] = None # fileFragmetToFeatureVector2Grams(fileFragment)
    retVal["conti"] = fileFragmentToFeatureVectorConti(fileFragment)
    retVal["compressed-length"] = fileFragmetToFeatureVectorCompressedLength(fileFragment)
    
    return retVal



if __name__ == "__main__":
    s = open("temp/000825-38.pdf", "r").read()
    t = ""
    for i in range(512):
	t += "\xff"
    print fileFragmentToFeatureVector(s)
    s.close()






