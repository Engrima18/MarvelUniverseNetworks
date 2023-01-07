#!/bin/bash

# 1.What is the most popular pair of heroes (often appearing together in the comics)?
first=$(cat dataset/archive/hero-network.csv | sort | uniq -c | grep -P '\d+ "(.*)","(?!\1)' | sort -n | tail -1)
read -r n heroes <<< $first
heroes=${heroes/,/ and }
echo Most popular pair of heroes are $heroes appearing together $n times!
echo 


# 2.Number of comics per hero.
echo Top 10 number of comics per superhero
awk -vFPAT='([^,]*)|("[^"]+")' -vOFS=, '{print $1}' dataset/archive/edges.csv | sort | uniq -c | sort -nr | head -10
echo
# COMMENT: we display only the first top ten. To have the all list just need to remove head or set a number of top heroes.


# 3.The average number of heroes in comics.
third=$(awk -vFPAT='([^,]*)|("[^"]+")' -vOFS=, '{print $2}' dataset/archive/edges.csv | sort | uniq -c | awk '{ tot += $1; nj++ } END { print tot/nj }')
echo The average number of heroes in comics is $third!

### RESULTS

# Most popular pair of heroes are "PATRIOT/JEFF MACE" and "MISS AMERICA/MADELIN" appearing together 1267 times!

#    1577 SPIDER-MAN/PETER PARKER
#    1334 CAPTAIN AMERICA
#    1150 IRON MAN/TONY STARK
#     963 THING/BENJAMIN J. GR
#     956 THOR/DR. DONALD BLAK
#     886 HUMAN TORCH/JOHNNY S
#     854 MR. FANTASTIC/REED R
#     835 HULK/DR. ROBERT BRUC
#     819 WOLVERINE/LOGAN
#     762 INVISIBLE WOMAN/SUE

# The average number of heroes in comics is 7.59603!