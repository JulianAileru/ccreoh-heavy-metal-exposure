"""
Notebook initialization for ST002118 analysis.
"""

# Standard library
import os
import sys
import platform
import warnings
from pathlib import Path
from itertools import chain
import re

# Third-party packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import patsy
from scipy import stats

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

warnings.simplefilter("ignore", FutureWarning)

SYSTEM = platform.system()

if SYSTEM == "Windows":
    METABOTKIT = Path(r"C:\Users\jaileru\Projects\metabolomics-toolkit")
    ROOT = Path(r"\\172.22.48.112\Sumner_HHEAR_Lichtveld\4a. Data_LC-MS_OrbiTrap\5-Statistical Analyses\Julian Analysis\July-2026")
elif SYSTEM == "Darwin":  # Mac
    # TODO: confirm these two against your actual Mac setup before first run.
    # METABOTKIT: wherever you've cloned/placed the toolkit repo locally.
    METABOTKIT = Path("/Users/julianaileru/GitHub/metabolomics-toolkit")
    # ROOT: the mount point for the same SMB share on Mac. Connect via
    # Finder > Go > Connect to Server > smb://172.22.48.112/Sumner_HHEAR_Lichtveld
    # then check what it actually mounts as under /Volumes/ (Finder will tell you,
    # or run `ls /Volumes` in Terminal after connecting).
    ROOT = Path("/Users/julianaileru/Library/CloudStorage/GoogleDrive-jaileru@researchallofus.org/My Drive/ST002118/Summer-2026")
else:
    raise OSError(f"Unhandled platform: {SYSTEM}")

if not ROOT.exists():
    warnings.warn(f"ROOT does not exist or is not mounted: {ROOT}")

PROJECT_ID = "ST002118"

# -----------------------------------------------------------------------------
# Add project paths
# -----------------------------------------------------------------------------

sys.path.append(str(METABOTKIT))
sys.path.append(str(ROOT / "Analysis"))

# Some IDE kernel launchers (e.g. Positron/VS Code) prepend their own bundled
# fallback packages to sys.path, which can shadow a newer version of the same
# package already installed in this environment (seen with typing_extensions
# vs. anndata's `sentinel` import). Force this interpreter's own site-packages
# to the front so environment-installed versions always win.
import sysconfig

_site_packages = sysconfig.get_paths()["purelib"]
if _site_packages in sys.path:
    sys.path.remove(_site_packages)
sys.path.insert(0, _site_packages)

# -----------------------------------------------------------------------------
# Project imports
# -----------------------------------------------------------------------------

from differential_abundance import DifferentialAbundance
from dimensionality_reduction import pca_plot, OPLSDA

# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------

__all__ = [
    # Packages
    "np",
    "pd",
    "sns",
    "plt",
    "px",
    "patsy",
    "stats",
    "chain",

    # Configuration
    "METABOTKIT",
    "ROOT",
    "PROJECT_ID",

    # Toolkit  -- uncomment once the imports above are live
    # "DifferentialAbundance",
    # "pca_plot",
    # "OPLSDA",

    # Reference maps / constants
    "ethnicity_map",
    "district_map",
    "maternal_age_map",
    "ptb_map",
    "lbw_map",
    "BIOMARKERS",
]

# -----------------------------------------------------------------------------
# Reference maps
# -----------------------------------------------------------------------------

ethnicity_map = {
    "1.0": "Creole",
    "2.0": "Hindustani",
    "3.0": "Indigenous",
    "4.0": "Javanese",
    "5.0": "Maroon",
    "6.0": "Mixed",
}

district_map = {
    "1.0": "Paramaribo",
    "2.0": "Wanica",
    "3.0": "Commewijne",
    "4.0": "Marowijne",
    "5.0": "Saramacca",
    "6.0": "Coronie",
    "7.0": "Nickerie",
    "8.0": "Para",
    "9.0": "Brokopondo",
    "10.0": "Sipaliwini",
}

maternal_age_map = {
    "1.0": "16-19 years",
    "2.0": "20-34 years",
    "3.0": "35+ years",
}

ptb_map = {
    "1.0": "yes",
    "2.0": "no",
}

lbw_map = {
    "1.0": "yes",
    "2.0": "no",
}

BIOMARKERS = {
    "EPA[OL-1]": ["15.53_285.2210m/z", "15.91_302.2244n"],
    "ArachidonicAcid[OL-1]": ["16.07_269.2260m/z", "16.23_304.2395n"],
    "DHA[OL-1]": "16.21_328.2395n",
    "DPA[OL-1]": "16.39_330.2554n",
    "AdrenicAcid[OL-1]": "16.64_332.2711n",
    "LinoleicAcid[OL-1]": ["16.24_280.2401n", "16.43_263.2366m/z"],
    "Linolenic[OL-1]": ["15.91_278.2243n", "16.45_306.2554n"],
    "TMAO[OL-1]": "0.64_75.0684n",
    "1-MethylHistidine[OL-2b]": ["1.67_169.0851n"],
}