#!/bin/bash

cd ..
vectorize.py -i ../fragments -o ../vectors/8k -n 8000 > /dev/null
echo "Done vectorizing 8k"
cd ../vectors/8k

intelligent_partition.py vector.svm
cp train.svm train_.svm
cp test.svm test_.svm
svm-scale -l 0 train_.svm > train.svm
svm-scale -l 0 test_.svm > test.svm
rm -f train_.svm test_.svm

svm-train -t 2 train.svm model.svm > /dev/null
svm-predict test.svm model.svm output.svm > results.txt
confusion.py > res.csv

svm-train -t 2 -c 100 train.svm model_big.svm > /dev/null
svm-predict test.svm model_big.svm output.svm > results_big.txt
confusion.py > res_big.csv

svm-train -t 2 -c 0.001 train.svm model_small.svm > /dev/null
svm-predict test.svm model_small.svm output.svm > results_small.txt
confusion.py > res_small.csv

echo "Done 8k!"
