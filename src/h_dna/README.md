triplex
conda install -y bioconductor-triplex bioconductor-rtracklayer bioconductor-genomicranges

Hseeker
pip install hseeker

TriplexFPP

git clone https://github.com/yuuuuzhang/TriplexFPP

conda install -c conda-forge numpy pandas biopython
pip install "tensorflow[and-cuda]"

triplexator
git clone https://github.com/Gurado/triplexator


cd triplexator
mkdir -p build/Release && cd build/Release

sed -i '933s/^/\/\//' src/seqan/file/file_generated_forwards.h
sed -i 's/::std::make_pair<unsigned,::std::pair< ::std::string,unsigned> >(seqNo,::std::make_pair< ::std::string,unsigned>(filename,seqNoWithinFile))/::std::make_pair(seqNo,::std::make_pair(filename,seqNoWithinFile))/g' src/triplexator.cpp

cmake ../.. -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=g++ -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DBoost_NO_BOOST_CMAKE=ON -DCMAKE_DISABLE_FIND_PACKAGE_Boost=ON -G "Unix Makefiles" && make
cd ../..

./bin/triplexator --help