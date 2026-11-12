# Landmark-based morphometrics in R: a beginner's tutorial

A hands-on R tutorial for analysing body measurements taken between anatomical landmarks, using simulated data from the whipworm *Trichuris muris* across its lifecycle.

It is written for **postgraduate students with little or no R experience**. You start with what R is, and finish fitting mixed-effects models and running a PCA. Every step has code to run, an explanation of what the analysis does and why, and a hidden "check your answer" box showing the result you should get.

> **The practice data are simulated.** They were generated to look realistic for teaching and are **not real measurements**. Everyone uses the same files, so every student gets identical numbers and figures.

## What you will learn

- Reading a spreadsheet into R, and turning an untidy lab sheet into a tidy table
- Quality-control checks that catch typing errors before any analysis
- Publication-quality figures with **ggplot2**
- Growth, body proportions and allometry (how body regions scale with body size)
- **Mixed-effects models** for worms nested within mice, and why ignoring the mouse gives misleading p-values
- **Principal component analysis (PCA)**, including separating size from shape

It also covers how to lay out your own data so that analysis is easy. An Excel template is included.

**Time needed:** about 6 to 8 hours, best spread over three sessions.

## Download

**Option 1: download a ZIP (no GitHub account or git needed)**

1. On this page, click the green **Code** button, then **Download ZIP**.
2. Unzip the file. You get a folder called `morphometrics_tutorial-main`. Put it somewhere sensible, such as your Documents folder. Avoid running it from inside the ZIP or from your Downloads folder.

**Option 2: clone with git**

```bash
git clone https://github.com/stephenrdoyle/morphometrics_tutorial.git
```

## Getting started

### 1. Install R and RStudio (once)

1. Install **R** (version 4.1 or newer; the latest is best) from <https://cran.r-project.org>.
2. Install **RStudio Desktop** (free) from <https://posit.co/download/rstudio-desktop/>.

### 2. Open the project

1. In the tutorial folder, double-click **`trichuris_morphometrics_tutorial.Rproj`**. RStudio opens with that folder as the working directory, which is what the code expects.
2. In RStudio's *Files* pane (bottom right), open **`trichuris_landmark_morphometrics_tutorial.Rmd`**.

### 3. Install the R packages (once)

Copy this into the RStudio **Console** (bottom left) and press Enter:

```r
install.packages(c("tidyverse", "patchwork", "emmeans", "lmerTest", "ggrepel", "rmarkdown", "knitr"))
```

It takes 5 to 10 minutes. If R asks *"Do you want to install from sources the packages which need compilation?"*, type `no` and press Enter.

### 4. Work through the tutorial

- **Step by step (recommended):** read a section, then run each grey code chunk with its green ▶ button. The output appears below the chunk.
- **All at once:** click **Knit** at the top of the editor to build the whole tutorial as a web page, with every output and figure.

If you're new to R, start with **"R in ten minutes"** near the top of the tutorial. If something goes wrong, the **"When something goes wrong"** table just after it covers the common errors.

## Checking your work

Under every figure and every key table there is a collapsed **"Check your figure"** or **"Check your output"** box. Run the code first, then open the box to compare. The expected figures are also in the `expected_figures/` folder, named after the code chunk that makes them.

The exercises at the end have hidden **Hint** boxes.

## What's in this repository

| Path | What it is |
|---|---|
| `trichuris_landmark_morphometrics_tutorial.Rmd` | The tutorial itself (R Markdown) |
| `trichuris_morphometrics_tutorial.Rproj` | RStudio project file: open this first |
| `START_HERE.txt` | A short plain-text version of these instructions |
| `data/` | The two practice CSV files (an untidy "lab sheet" and the tidy version) and a README describing them |
| `expected_figures/` | What each figure should look like once you have run its code |
| `template/` | An Excel template for entering your own measurements in the tidy layout, with drop-down lists, a data dictionary and an example sheet |
| `tools/` | The Python script that generated the practice data (not needed for the tutorial) |

## Using your own data

1. Enter your measurements in `template/trichuris_morphometrics_data_template.xlsx`, one row per worm.
2. Save the `data` sheet as **CSV UTF-8**, in the `data/` folder.
3. Point Section 3.4 of the tutorial at your file, and run the rest.

If your data are already in a different spreadsheet layout, Section 3 shows how to convert them.

## Reproducibility

The tutorial and expected outputs were generated with R 4.5.0 on macOS, with tidyverse 2.0.0, ggplot2 4.0.3, lme4 2.0-6, lmerTest 3.2-1, emmeans 2.0.4, patchwork 1.3.2 and ggrepel 0.9.8. Random elements (jittered points, label placement) use fixed seeds, so the figures should match exactly. A PCA axis may occasionally come out mirror-imaged on a different computer. That doesn't change the interpretation, and the tutorial says so where it matters.

The practice data can be regenerated exactly with `python tools/make_simulated_data.py` (requires numpy and pandas; fixed seed 2026).

## Contact

Stephen Doyle, Wellcome Sanger Institute. Questions and corrections are welcome as [GitHub issues](https://github.com/stephenrdoyle/morphometrics_tutorial/issues).
