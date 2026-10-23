suppressPackageStartupMessages({
  suppressWarnings({
    library("triplex", quietly = TRUE, verbose = FALSE)
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

triplex_res <- triplex.search(
  seq,
  min_len = 10,
  max_len = 30,
  min_loop = 1,
  max_loop = 10
)

triplex_res_gr <- as(triplex_res, "GRanges")

export(
  triplex_res_gr,
  output_file,
  format = "BED"
)