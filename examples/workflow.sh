#!/bin/bash

OLD=./
NEW=Fe46Pt08

for POSCAR in $(awk '{print $1}' ${OLD}/cell.in); do
  python3 ../EXPAND_CELL.py --help
  echo python3 ../EXPAND_CELL.py ${OLD}/${POSCAR} 8 Pt Fe 12800 _${NEW}
  python3      ../EXPAND_CELL.py ${OLD}/${POSCAR} 8 Pt Fe 12800 _${NEW}
done                                                      || exit

python3 ../_symmetry.py --help
echo python3 ../_symmetry.py _${NEW} ${NEW} delete        || exit
python3      ../_symmetry.py _${NEW} ${NEW} delete        || exit
rm -r _${NEW}                                             || exit
if [ -s different_directory.txt ]; then
    NEW=$(cat different_directory.txt)
    rm different_directory.txt
fi

cd ${NEW}                                                 || exit
echo sh ../../_combine_stats.sh                           || exit 
sh ../../_combine_stats.sh                                || exit 
echo sh ../../_unique.sh                                  || exit 
sh ../../_unique.sh                                       || exit 
rm -r [0-9]*                                              || exit 
mv unique/* ./                                            || exit 
rm -r unique                                              || exit 
echo python3 ../../_correlation_function.py ./ radial yes || exit 
python3      ../../_correlation_function.py ./ radial yes || exit 
