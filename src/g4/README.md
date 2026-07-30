pqsfinder
Install R and then use conda

conda install -c conda-forge -c bioconda -y bioconductor-pqsfinder

G4Hunter

For Python 3 support:

git clone https://github.com/Georgakopoulos-Soares-lab/G4Hunter-Companion
cd g4hunter
conda install -c conda-forge -c bioconda pybedtools datrie bedtools
pip install -e .