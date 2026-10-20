args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 3) {
  stop("Usage: Rscript quadron.R <input.fasta> <output.txt> <quadron.lib>", call. = FALSE)
}

input_file <- args[1]
output_file <- args[2]
quadron_lib <- args[3]

print("NOTE: Loading Quadron core...", quote=FALSE)
load(quadron_lib)

Quadron(
  FastaFile = input_file, 
  OutFile = output_file,
  nCPU = 1
)