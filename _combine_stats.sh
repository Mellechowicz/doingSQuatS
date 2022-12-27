#!/bin/bash

DIR=$PWD

while [ "${DIR}" != "${HOME}" ]; do
  if [ -s ${DIR}/_compare.py ]; then
    CMP="${DIR}/_compare.py"
    echo "Found _compare.py @ $CMP"
    break
  fi
  DIR=$(dirname $DIR)
done

if [ ! -s $CMP ]; then
  echo 'I have not found _compare.py!'
  exit
fi

if [ -n "$1" ]; then
  DIRS="$@"
else
  DIRS="*"
fi


for d in ${DIRS}; do
(
  cd $d 2> /dev/null || exit
  toilet -f pagga $d
  if [ ! -s statistcs.txt ]; then
    python3 ${CMP} #& disown
  fi
  toilet -f pagga "$d done"
)
done

(for d in ${DIRS}; do
(
  cd $d 2> /dev/null || exit
  if [ -s statistcs.txt ]; then
    awk -v D=$d '{print D,$0}' statistcs.txt
  fi
)
done) | sort -n -k3 > probability.txt

MAX=$(awk 'BEGIN{s=0} {s+=$3} END{print s}' probability.txt)
awk -v max=${MAX} '{print $0,$3*100.0/max}' probability.txt
