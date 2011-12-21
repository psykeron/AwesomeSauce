#!/bin/bash

cd ..
vectorize.py -i ../fragments -o ../vectors/1k -n 1000 > /dev/null
echo "Done vectorizing 1k"
cd ../vectors/1k

intelligent_partition.py vector.svm
cp train.svm train_.svm
cp test.svm test_.svm
svm-scale -l 0 train_.svm > train.svm
svm-scale -l 0 test_.svm > test.svm
rm -f train_.svm test_.svm

svm-train -t 2 train.svm model.svm > /dev/null
svm-predict test.svm model.svm output.svm > results.txt
confusion.py > res.csv
echo "Done 1k!"
