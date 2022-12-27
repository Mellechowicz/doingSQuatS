#!/bin/bash

if [ ! -n "$1" ]; then
	echo "(i) How many dirs"
	exit
fi

for s in $(seq 1 $1); do
	S="000$s"
	S=${S: -4}
	mkdir $S
done

for f in $(ls $MASK | grep vasp); do
  DLT=$(gsl-randist $RANDOM 1 flat 0 $1)
  S="000$(echo $DLT | awk -v MAX=$1 '{for(i=1;i<=MAX;i++){if($1<i){print i; exit}}}')"
  S=${S: -4}
  mv $f $S
  echo -n '.'
done

echo ' done'
