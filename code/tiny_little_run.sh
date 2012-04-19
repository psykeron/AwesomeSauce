#! /bin/sh

VECTOR_FILE='vector.svm'
TRAIN_FILE='train.svm'
TEST_FILE='test.svm'
MODEL_FILE='model.svm'
OUTPUT_FILE='output.svm'
RESULTS_FILE='results.txt'
RES_FILE='res.csv'

INPUT_DIR=${1}
OUTPUT_DIR=${2}
NUM_FRAGMENTS=${3}
feature=${4}

TARGET_DIR="${OUTPUT_DIR}/feature${feature}/run${5}"

echo "feature${feature}/run${5}: Vectorizing..."
python ./vectorize.py -i "${INPUT_DIR}" -o "${TARGET_DIR}" -n ${NUM_FRAGMENTS} --omit ${feature} > /dev/null

echo "feature${feature}/run${5}: Partitioning..."
python ./intelligent_partition.py --train-fname "${TARGET_DIR}/${TRAIN_FILE}" --test-fname "${TARGET_DIR}/${TEST_FILE}" "${TARGET_DIR}/${VECTOR_FILE}" > /dev/null

echo "feature${feature}/run${5}: Training..."
svm-train -t 0 "${TARGET_DIR}/${TRAIN_FILE}" "${TARGET_DIR}/${MODEL_FILE}" > /dev/null

echo "feature${feature}/run${5}: Testing..."
svm-predict "${TARGET_DIR}/${TEST_FILE}" "${TARGET_DIR}/${MODEL_FILE}" "${TARGET_DIR}/${OUTPUT_FILE}" > "${TARGET_DIR}/${RESULTS_FILE}"
python ./confusion.py -p "${TARGET_DIR}/${OUTPUT_FILE}" -t "${TARGET_DIR}/${TEST_FILE}" > "${TARGET_DIR}/${RES_FILE}"
