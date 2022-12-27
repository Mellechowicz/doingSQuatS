#!/bin/bash

if [ -n "$1" ]; then
  MASK="*${1}*"
else
  MASK=""
fi

for f in $(ls $MASK | grep vasp); do
  DLT=$(gsl-randist $RANDOM 1 gaussian 0.7803051)
  DLT=$(echo $DLT | awk '{if($1<1.0){print "yes"}else{print "no"}}')
  if [ "$DLT" == 'yes' ]; then
    rm -f $f
  fi
done
