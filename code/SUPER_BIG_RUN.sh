#! /bin/sh

# do everything!

# be careful!!

INPUT_DIR='/p/theory/oles/project/AwesomeSauce/code/random_fragments4'
OUTPUT_DIR=${1}
NUM_FRAGMENTS='1000'

if [ ! -d "${OUTPUT_DIR}" ]
then
  mkdir "${OUTPUT_DIR}"
else
  echo "${0}: ${OUTPUT_DIR} already exists! Fix it! Exiting..."
  exit 1
fi

for feature in -1 0 1 2 3 4 5 6 7
do

  mkdir "${OUTPUT_DIR}/feature${feature}"

  for run_number in 0 1 2
  do

    mkdir "${OUTPUT_DIR}/feature${feature}/run${run_number}"

    ./tiny_little_run.sh ${INPUT_DIR} ${OUTPUT_DIR} ${NUM_FRAGMENTS} ${feature} ${run_number} &

  done

done



