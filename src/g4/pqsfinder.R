suppressPackageStartupMessages({
  suppressWarnings({
    library("pqsfinder", quietly = TRUE, verbose = FALSE)
    library("rtracklayer", quietly = TRUE, verbose = FALSE)
    library("GenomicRanges", quietly = TRUE, verbose = FALSE)
  })
})

args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 2) {
  stop("Usage: Rscript triplex.R <input.fasta> <output.bed>", call. = FALSE)
}

input_file <- args[1]
output_file <- args[2]

seqs <- readDNAStringSet(input_file)
seq <- seqs[[1]]

pqs_res <- pqsfinder::pqsfinder(
  seq,
  max_bulges = 0,
  run_min_len = 3,
  run_max_len = 4,
  loop_min_len = 1,
  loop_max_len = 9  
)
pqs_gr <- as(pqs_res, "GRanges")

rtracklayer::export(
  pqs_gr,
  output_file,
  format = "BED"
)