#!/bin/bash

# Define the directory to download the T2T-CHM13v2.0 assembly
data_dir="../data"

# Obtain it from the NCBI Genome database and unzip 
wget \
    -O $data_dir/chm13_assembly.fna.gz \
    "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/914/755/GCF_009914755.1_T2T-CHM13v2.0/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna.gz"

gunzip $data_dir/chm13_assembly.fna.gz

# Index the fasta file using SAMTools
samtools faidx $data_dir/chm13_assembly.fna

# Extract the sequence only of chromosome 18 to use in the benchmarking
samtools faidx $data_dir/chm13_assembly.fna NC_060942.1 > $data_dir/chr18.fa
