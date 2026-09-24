
library(MetaboAnalystR)
setwd("/Users/julianaileru/Library/CloudStorage/GoogleDrive-jaileru@researchallofus.org/My Drive/ST002118/July-2026/Analysis/PathwayAnalysis")

PathwayAnalysis <- function(pvalue,rt,ion_mode,input_path,output_path,name_output_file){
  dpi <- 150
  format <- "png"
  imgName <- paste0(output_path, "dpi", dpi, ".", format)

  matched_compound_csv <- "mummichog_matched_compound_all.csv"
  pathway_enrichment_csv <- "mummichog_pathway_enrichment_mummichog.csv"

  matched_compound_dest <- paste0(name_output_file, "_matched_compound_all.csv")
  pathway_enrichment_dest <- paste0(name_output_file, "_pathway_enrichment_mummichog.csv")

  keep_files <- c(
    imgName,
    matched_compound_csv,
    pathway_enrichment_csv
  )

  before_files <- list.files(getwd())

  mSet<-InitDataObjects("mass_all", "mummichog", FALSE, 150)
  mSet<-SetPeakFormat(mSet, "rmp")
  mSet<-UpdateInstrumentParameters(mSet, rt, ion_mode, "yes", 0.02);
  mSet<-Read.PeakListData(mSet, input_path);
  mSet<-SanityCheckMummichogData(mSet)
  mSet<-SetPeakEnrichMethod(mSet, "mum", "v2")
  mSet<-SetMummichogPval(mSet, pvalue)
  mSet<-PerformPSEA(mSet, "hsa_kegg", "current", 3 , 100)
  mSet<-PlotPeaks2Paths(mSet, output_path, format, dpi, width=NA)

  after_files <- list.files(getwd())
  junk_files <- setdiff(after_files, union(before_files, keep_files))
  if (length(junk_files) > 0) {
    file.remove(junk_files)
  }

  if (file.exists(matched_compound_csv)) {
    file.rename(matched_compound_csv, matched_compound_dest)
  }
  if (file.exists(pathway_enrichment_csv)) {
    file.rename(pathway_enrichment_csv, pathway_enrichment_dest)
  }

  invisible(mSet)
}

output_dir <- "output/080526"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

input_files <- list.files("input/080526", pattern = "input-T1-080526\\.txt$", full.names = TRUE)

for (input_path in input_files) {
  base_name <- tools::file_path_sans_ext(basename(input_path))
  output_base <- sub("input", "output", base_name)
  output_path <- file.path(output_dir, output_base)

  PathwayAnalysis(
    pvalue = 0.05,
    rt = 3.0,
    ion_mode = "positive",
    input_path = input_path,
    output_path = output_path,
    name_output_file = output_path
  )
}

input_files <- list.files("input/080526", pattern = "input-T2-080526\\.txt$", full.names = TRUE)

for (input_path in input_files) {
  base_name <- tools::file_path_sans_ext(basename(input_path))
  output_base <- sub("input", "output", base_name)
  output_path <- file.path(output_dir, output_base)

  PathwayAnalysis(
    pvalue = 0.05,
    rt = 3.0,
    ion_mode = "positive",
    input_path = input_path,
    output_path = output_path,
    name_output_file = output_path
  )
}