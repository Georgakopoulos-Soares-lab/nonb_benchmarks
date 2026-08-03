pqsfinder
Install R and then use conda

conda install -c conda-forge -c bioconda -y bioconductor-pqsfinder

G4Hunter

For Python 3 support:

git clone https://github.com/Georgakopoulos-Soares-lab/G4Hunter-Companion
cd g4hunter
conda install -c conda-forge -c bioconda pybedtools datrie bedtools
pip install -e .

Quadron
installation instructions from https://github.com/aleksahak/Quadron

install.packages("plyr")
install.packages("data.table")
install.packages("caret")
install.packages("shiny")
install.packages("doMC")
install.packages("foreach")
install.packages("itertools")

git clone https://github.com/aleksahak/Quadron (big repo takes a while to clone)

install.packages(
    "http://cran.r-project.org/src/contrib/Archive/xgboost/xgboost_0.4-4.tar.gz",
    repos=NULL,
    type="source")

cd Quadron/lib/
in R
source("bitcompile.R") 

G4Boost requires python 3.9 and not more recent builds since it breaks requirements

git clone https://github.com/hbusra/G4Boost.git
cd G4Boost

conda create -p g4boost -c conda-forge python=3.9 numpy=1.23 pandas=1.4.3 scikit-learn=1.0.2 py-xgboost=1.4.2

G4detector

git clone https://github.com/OrensteinLab/G4detector
Keras 2.1.6 using Tensorflow backend