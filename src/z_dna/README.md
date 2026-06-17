ZSeeker install
from https://github.com/Georgakopoulos-Soares-lab/ZSeeker
install python 3.11
pip install ZSeeker

Z-GENIE
from https://github.com/agarzare/Z-GENIE

install R

clone repository
git clone https://github.com/agarzare/Z-GENIE.git

install.packages("devtools")
devtools::install("ZGENIE")

Z-HUNT
from: https://github.com/Ho-Lab-Colostate/zhunt

git clone https://github.com/Ho-Lab-Colostate/zhunt

cd zhunt
gcc -O2 -o bin/zhunt zhun3.c -lm
./bin/zhunt 12 6 12 /work2/10901/lefteris/stampede3/nonb_benchmarks/data/chr18.fa