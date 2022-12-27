#!/bin/bash

if [ -s /home/andrzej/andrzej/sSQSgenerator/_compare.py ]; then
  CMP='/home/andrzej/andrzej/sSQSgenerator/_compare.py'
elif [ -s /home/andrzej/MEGAsync/sSQSgenerator/_compare.py ]; then
  CMP='/home/andrzej/MEGAsync/sSQSgenerator/_compare.py'
elif [ -s /home/andrzej/alloys/sSQSgenerator/_compare.py ]; then
  CMP='/home/andrzej/alloys/sSQSgenerator/_compare.py'
else
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
    ${CMP} #& disown
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
