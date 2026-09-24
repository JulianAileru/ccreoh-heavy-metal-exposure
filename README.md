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
  - Prediction Task?
  - WQS Regression (looking at combined effect of metals?) 

