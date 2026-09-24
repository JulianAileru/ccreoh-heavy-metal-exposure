# Analysis Plan
## Meet-In-The-Middle-Analysis
  - Metals-MWAS: models each signal’s intensity as the outcome and metal concentration as the primary predictor, while adjusting for relevant covariates.
    ### Metal-MWAS Model
    -     Metabolite(i) ~ Metal(i) + BMI +
          Maternal Age at Intake + Maternal Education Level +
          Ethnicity + Household Income
  - Pathway Enrichment Analysis: Mummichog identifies enriched pathways without the need for formal annotation of compounds
    - Enrichment analysis was performed per metal to observe pathway perturbations associated with Metals
    - Settings:
        - Pathway Database: KEGG (human)
        - Ion Mode: Positive
        - Mass Tolerance: 3.0 (ppm)
        - Retention Time: Yes
  - Outcome Model: looks for the association between the health outcome (__Gestational Age At Birth__, __Birthweight__) and each metabolite while adjusting for covariates
    ### Outcome Model
    -     Gestational Age at Birth/Birthweight ~ Metabolite(i) + BMI +
          Maternal Age at Intake + Maternal Education Level +
          Ethnicity + Household Income
    - Filtering Approach: Apply FDR correction with cutoff q = 0.2 for Metals-MWAS, then for the Outcome Models do not apply a cutoff.
## Gordon Conference 
  - Abstract Submitted and Accepted: [Abstract](<Info/Abstract (ST002118) - 08.18.26>)
## Further Analysis
  ### Scope for this paper
  - Build on the single-metal MWAS with a **mixture MWAS**. Goal: characterize how the 5-metal mixture perturbs the metabolome and which of those perturbations are also associated with the outcomes.
  - Framing: the original BKMR paper showed the metal mixture is associated with the health outcomes; this paper is a hypothesis-generating follow-up on the metabolome. It does **not** claim mediation.
  - BKMR across all ~9,000 features is not feasible, so mixture effects are screened with fast per-feature models and BKMR is reserved for a small shortlist.

  ### Planned Workflow
  1. **Single-metal MWAS (done).** Baseline for comparison.
  2. **Mixture MWAS.** Per feature, fit a mutually adjusted model with all 5 metals (and/or qgcomp with `degree = 1`).
     - Mutually adjusted model:
       -     Metabolite(i) ~ Metal1 + Metal2 + Metal3 + Metal4 + Metal5 + BMI +
             Maternal Age at Intake + Maternal Education Level +
             Ethnicity + Household Income
     - Joint F-test per feature (H0: all five metal coefficients = 0). Detects any association with the mixture, including mixed directions.
     - Overall mixture effect (ψ) per feature: sum of the five coefficients, i.e. the expected change in the metabolite when all metals increase by one unit/quantile. Can be obtained from qgcomp or as a linear combination of coefficients. Net effect, so opposing metals can cancel.
     - qgcomp version: `Metabolite(i) ~ q(Metal1..Metal5) + covariates`. Gives ψ, its CI/p-value, and positive/negative weights.
     - Apply FDR (q < 0.2) to the mixture-level result (one test per feature).
     - **Decide before looking at results:** which test is primary (F-test vs. ψ). If mixed directions are expected, F-test is the safer primary and ψ is reported alongside it.
  3. **Compare single-metal vs. mixture results.**
     - Features significant in single-metal models but not after mutual adjustment: likely driven by co-exposure.
     - Features significant only in the mixture model: possible joint or suppressed effects.
     - Visuals: Venn/UpSet plot of hits, effect-size concordance by metal (single-metal vs. mutually adjusted).
  4. **Pathway enrichment on mixture hits.**
     - Rerun Mummichog on mixture-level p-values (same settings as above: KEGG human, positive mode, 3 ppm, RT = Yes).
     - Mummichog does not use direction, so mixture-level enrichment shows which pathways are perturbed, not which way. Use per-metal enrichment from the mutually adjusted model for directional detail.
     - Compare against per-metal runs. Pathways found in both are the strongest results.
  5. **Outcome models on the shortlist (meet-in-the-middle).**
     - Restrict the outcome models (Gestational Age at Birth, Birthweight) to mixture-associated features, keeping the original design.
     - Consider applying FDR within this subset so there is a significance statement for the outcome step.
     - Check direction consistency (metal ↑ → metabolite ↑/↓ → outcome ↑/↓) and describe as overlap, not mediation.
  6. **BKMR on a handful of top features (optional).**
     - Metabolite as outcome, 5 metals as the kernel term, top features only (SLURM array job).
     - Provides exposure-response shapes, interactions (e.g., pairwise metal interactions), and PIPs.
     - Compare PIPs/weights with the original BKMR paper; agreement strengthens the story and disagreement is worth discussing.

  ### Sensitivity Analyses
  - **Non-linearity test (one per feature):** compare the linear model to a flexible model with natural splines (df = 3) or `mgcv` smooths on each metal, using a nested F-test/LRT. FDR-correct across features.
    - Summarize with the p-value histogram, Storey's π₀, number of features passing FDR, and change in R²/AIC.
    - Null results mean "no evidence of non-linearity" (power is limited), not "linear."
    - Use the original BKMR exposure-response plots as a prior for which metals to look at first.
  - **qgcomp `degree = 2`** (uses `qgcomp.boot`): checks whether hit list and mixture findings change with squared terms. Does not capture metal × metal interactions unless added explicitly to the formula.
  - **Alternative FDR cutoffs** around q = 0.2 and bootstrap stability of selected features.
  - **Metal correlation structure:** report the correlation matrix and VIFs; high correlation inflates variance under mutual adjustment.
  - **Additional covariates to consider:** infant sex, gestational age at sample collection, batch/plate, smoking, parity. For birthweight, adjust for gestational age or use GA-standardized z-scores (e.g., INTERGROWTH).
  - **Effect modification:** metal × infant sex interactions.
  - **Feature preprocessing checks:** confirm log-transformation/normalization and check for high-leverage points before interpreting curves.
  - **Annotation confidence:** Mummichog pathway results are putative; confirm key metabolites with MS/MS or standards if reporting them.

  ### Open Decisions / Info Needed
  - Total sample size and number of metals (5) to confirm the feasibility of spline tests and BKMR.
  - Primary mixture test (joint F-test vs. ψ).
  - Timing of metal and metabolomics collection relative to birth (matters for any later mediation claims).
  - Whether to add the additional covariates above.

  ### Future Directions (not in this paper)
  - **Mediation analysis** (Q: how does metal influence outcome through the metabolome?)
    - Run only on a shortlist of features: HIMA-type screening for high-dimensional mediators, or BKMR-based causal mediation (Devick et al., 2022) for the top candidates.
    - Requires no unmeasured confounding on the metal-outcome, metal-metabolite, and metabolite-outcome paths, plus a defensible temporal ordering. Frame results as "consistent with mediation."
  - **Prediction task** (Q: can the metabolome predict Preterm Birth or abnormal birthweight?)
    - Elastic net with nested cross-validation; compare against a covariates-only baseline; report calibration as well as AUC.
    - Split into training/test sets before any feature selection.
    - Depends on case counts. Model micro- and macrosomia separately (or as a 3-class model, or continuous birthweight/GA z-score) rather than combining them as "abnormal."
    - Signature score can later be used as a single outcome in BKMR with the 5 metals to link back to the mixture question.
  - **Metabolite-set qgcomp/WQS on the outcome:** use a pre-selected set (overlap features, enriched pathway, or WGCNA/xMWAS module) as the mixture, with separate selection and estimation samples. WQS assumes a single direction, so qgcomp is preferred unless BKMR results show metals act in one direction.
  - **Dimension reduction:** WGCNA/xMWAS modules or pathway-level scores to reduce multiple testing.
  - **Alternative outcomes:** preterm birth, SGA/LGA, birthweight-for-GA z-scores.
  - **External or split-sample replication** if available.


