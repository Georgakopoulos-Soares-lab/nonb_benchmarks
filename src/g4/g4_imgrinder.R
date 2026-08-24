suppressPackageStartupMessages({
  suppressWarnings({
    library("G4iMGrinder", quietly = TRUE, verbose = FALSE)
    library("rtracklayer", quietly = TRUE, verbose = FALSE)
    library("GenomicRanges", quietly = TRUE, verbose = FALSE)
  })
})

args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 2) {
  stop("Usage: Rscript g4_imgrinder.R <input.fasta> <output.csv>", call. = FALSE)
}

input_file <- args[1]
output_file <- args[2]

Sequence <- paste0(
  seqinr::read.fasta(file = input_file, as.string = TRUE, 
                     legacy.mode = TRUE, seqonly = TRUE, 
                     strip.desc = TRUE), 
  collapse = ""
)

res <- G4iMGrinder(Name = "chr18", Sequence = Sequence, NCores = 1)
write.csv(res$PQSM2a, output_file, row.names = FALSE)