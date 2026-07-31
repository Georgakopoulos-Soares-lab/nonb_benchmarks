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

Z-DNABERT
code from https://github.com/mitiau/Z-DNABERT/blob/main/ZDNA-prediction.ipynb
pip install transformers biopython gdown scipy
pip install torch --index-url https://download.pytorch.org/whl/cu126

gdown 1VAsp8I904y_J0PUhAQqpSlCn1IqfG0FB --output models/HG_chipseq/
gdown 1dAeAt5Gu2cadwDhbc7OnenUgDLHlUvkx --output models/HG_kouzine/
gdown 1W6GEgHNoitlB-xXJbLJ_jDW4BF35W1Sd --output models/MM_curax/
gdown 1dXpQFmheClKXIEoqcZ7kgCwx6hzVCv3H --output models/MM_kouzine/

gdown 10sF8Ywktd96HqAL0CwvlZZUUGj05CGk5 
gdown 16bT7HDv71aRwyh3gBUbKwign1mtyLD2d
gdown 1EE9goZ2JRSD8UTx501q71lGCk-CK3kqG
gdown 1gZZdtAoDnDiLQqjQfGyuwt268Pe5sXW0

