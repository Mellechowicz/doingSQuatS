#!/bin/bash

mkdir -p unique
if [ -s probability.txt ]; then
		for i in $(seq 1 $(grep -c vasp probability.txt)); do
				D=$(sed "${i}q;d" probability.txt | awk '{print $1}')
				F=$(sed "${i}q;d" probability.txt | awk '{print $2}')
				cp $D/$F unique/${D}_${F}
				if [ -n "$1" ]; then
					rm $D/$F
				fi
		done
fi
