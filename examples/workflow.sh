#!/bin/bash

OLD=./
NEW=Fe38Pt16

for POSCAR in $(awk '{print $1}' ${OLD}/cell.in); do
  python3 ../EXPAND_CELL.py --help
  python3 ../EXPAND_CELL.py ${OLD}/${POSCAR} 16 Pt Fe 128000 _${NEW}
done                                         || exit

../_symmetry.py _${NEW} ${NEW} delete        || exit
rm -r _${NEW}                                || exit

cd ${NEW}                                    || exit
../../_combine_stats.sh                      || exit 
../../_unique.sh                             || exit 
rm -r [0-9]*                                 || exit 
mv unique/* ./                               || exit 
rm -r unique                                 || exit 
../../_correlation_function.py ./ radial yes || exit 
