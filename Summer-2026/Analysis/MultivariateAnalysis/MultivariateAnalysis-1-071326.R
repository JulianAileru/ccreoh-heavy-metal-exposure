library(ropls)
library(dplyr)
library(arrow)
library(readxl)
library(tibble)
setwd(R"(\\172.22.48.112\Sumner_HHEAR_Lichtveld\4a. Data_LC-MS_OrbiTrap\5-Statistical Analyses\Julian Analysis\July-2026\)")
# Targeted Data OPLS-DA
targeted <- read_excel(R"(Data\Targeted\TARGETED_DATA_WIDE_07132026.xlsx)")
categorical <- read_parquet("Analysis\\MultivariateAnalysis\\CategoricalDataForR.parquet")

categorical <- categorical %>%
  select(-"Hg (ng/mL)")

t1_samples <- intersect(targeted$SID_MW,categorical$`__index_level_0__`)

t1_targeted <- targeted[targeted$SID_MW %in% t1_samples,]

t1_targeted_subset <- t1_targeted %>%
  select(
    SID_MW,
    contains("ng/mL")
  )


dat <- t1_targeted_subset %>%
  inner_join(
    categorical %>% rename(SID_MW = `__index_level_0__`),
    by = "SID_MW"
  )

epa <- factor(dat$"Hg EPA")
X <- dat %>%
  select(contains("ng/mL"))

keep <- complete.cases(X)
X <- X[keep,]
y <- epa[keep]

X <- as.matrix(X)

opls_model <- opls(X,y,predI=1,orthoI = NA)
plot(opls_model, typeVc = "x-score")
vip <- getVipVn(opls_model)
vip_df <- data.frame(
  Metabolite = names(vip),
  VIP = vip
) %>%
  arrange(desc(VIP))




dat_tb <- dat %>%
  filter(`Hg Tertiles` %in% c("T1", "T4"))
y <- factor(dat_tb$`Hg Tertiles`)
X <- dat_tb %>%
  select(ends_with("(ng/mL)"))


X <- log2(X)

keep <- complete.cases(X)

X <- as.matrix(X[keep, ])
y <- y[keep]

opls_model <- opls(
  X,
  y,
  predI = 1,
  orthoI = NA,
  permI = 100
)
plot(opls_model, typeVc = "x-score")
vip <- getVipVn(opls_model)
vip_df <- data.frame(
  Metabolite = names(vip),
  VIP = vip
) %>%
  arrange(desc(VIP))
