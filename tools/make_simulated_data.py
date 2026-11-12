"""
Generate the two practice CSVs that ship with the Trichuris muris morphometrics tutorial.

  data/trichuris_muris_landmarks_messy.csv   spreadsheet-style file (untidy on purpose)
  data/trichuris_muris_landmarks_tidy.csv    the same worms in the tidy template layout

Everything is simulated and illustrative: these are NOT real measurements.
Fixed seed, so re-running this script reproduces the files exactly.
Requires: numpy, pandas.
"""
import numpy as np
import pandas as pd
from pathlib import Path

SEED = 2026
base = Path(__file__).resolve().parent
if base.name == "tools":          # when stored in <project>/tools/, write to <project>/data/
    base = base.parent
out = base / "data"
out.mkdir(exist_ok=True)
rng = np.random.default_rng(SEED)

# ------------------------------------------------------------------ design
# (dpi, lifestage group, mean whole-body length in um, number of worms)
design = [
    (0,  "L1 (newly hatched)",   220, 30),
    (3,  "L1",                   280, 20),
    (9,  "L2",                   700, 20),
    (14, "L3",                  1500, 25),
    (21, "L4",                  4500, 25),
    (35, "Adult female",       25000, 30),
    (35, "Adult male",         20000, 30),
    (42, "Adult female",       28000, 25),
    (42, "Adult male",         22000, 25),
]
# mean proportion of the body in each region (rows sum to 1):
# ant_nr, nr_st, st, intestine, ov_ts, rt_cl, rest
props = {
    "L1 (newly hatched)": [0.10, 0.08, 0.38, 0.30, 0.00, 0.04, 0.10],
    "L1":                 [0.10, 0.08, 0.38, 0.30, 0.00, 0.04, 0.10],
    "L2":                 [0.09, 0.08, 0.40, 0.28, 0.00, 0.04, 0.11],
    "L3":                 [0.08, 0.07, 0.44, 0.25, 0.02, 0.03, 0.11],
    "L4":                 [0.06, 0.06, 0.48, 0.22, 0.05, 0.03, 0.10],
    "Adult female":       [0.04, 0.04, 0.52, 0.18, 0.12, 0.02, 0.08],
    "Adult male":         [0.04, 0.04, 0.52, 0.19, 0.06, 0.02, 0.13],
}
region_cols = ["ant_nr", "nr_st", "st", "intestine", "ov_ts", "rt_cl", "rest"]

# ------------------------------------------------------------------ mice
# each mouse is culled at ONE timepoint (mice nested within dpi);
# larvae at dpi 0 were hatched in vitro and have no host
mice = pd.DataFrame({"dpi": np.repeat([3, 9, 14, 21, 35, 42], [4, 4, 5, 5, 5, 5])})
mice["host_id"] = [f"M{i + 1:02d}" for i in range(len(mice))]
mice["mouse_size"] = rng.normal(0, 0.08, len(mice))      # mouse shifts worm size
mice["mouse_st_effect"] = rng.normal(0, 0.06, len(mice))  # ... and relative stichosome length
pool = mice.groupby("dpi")["host_id"].apply(list).to_dict()
mouse_lookup = mice.set_index("host_id")

# ------------------------------------------------------------------ worms
rows = [(d, ls, m) for d, ls, m, n in design for _ in range(n)]
df = pd.DataFrame(rows, columns=["dpi", "lifestage", "mean_length_um"])
N = len(df)
df["sample"] = [f"S{i + 1:03d}" for i in range(N)]
df["host_id"] = [rng.choice(pool[d]) if d in pool else None for d in df["dpi"]]
mouse_size = df["host_id"].map(mouse_lookup["mouse_size"]).fillna(0.0).to_numpy()
mouse_st = df["host_id"].map(mouse_lookup["mouse_st_effect"]).fillna(0.0).to_numpy()

wb = df["mean_length_um"].to_numpy() * np.exp(mouse_size + rng.normal(0, 0.08, N))

P = np.array([props[ls] for ls in df["lifestage"]], dtype=float)
P[:, 2] *= np.exp(mouse_st)                     # relative stichosome length varies by mouse
P *= np.exp(rng.normal(0, 0.08, P.shape))       # individual variation in every proportion
P /= P.sum(axis=1, keepdims=True)               # rescale so proportions sum to 1

lengths = P * wb[:, None]
df["wb_length"] = wb
for k, c in enumerate(region_cols):
    df[c] = lengths[:, k]
df["ant_st"] = df["ant_nr"] + df["nr_st"]

df["ant_nr_pct"] = P[:, 0] * 100
df["nr_st_pct"] = P[:, 1] * 100
df["ant_st_pct"] = df["ant_st"] / df["wb_length"] * 100
df["st_pct"] = P[:, 2] * 100
df["intestine_pct"] = P[:, 3] * 100
df["ov_ts_pct"] = P[:, 4] * 100
df["rt_cl_pct"] = P[:, 5] * 100
df["rest_pct"] = P[:, 6] * 100

df["st_number"] = np.round(8 + 38 * (1 - np.exp(-wb / 4000)) + rng.normal(0, 3, N))
meas_set = rng.choice(["length_only", "head", "full"], size=N, p=[0.35, 0.25, 0.40])
keep_st = (meas_set == "full") & (~df["lifestage"].isin(["L1 (newly hatched)", "L1"])) \
          & (rng.random(N) < 0.6)
df.loc[~keep_st, "st_number"] = np.nan

# partial measurement: head landmarks only, or length only
head = ["ant_nr", "nr_st", "ant_st", "ant_nr_pct", "nr_st_pct", "ant_st_pct"]
body = ["st", "intestine", "ov_ts", "rt_cl", "rest",
        "st_pct", "intestine_pct", "ov_ts_pct", "rt_cl_pct", "rest_pct"]
df.loc[meas_set == "length_only", head] = np.nan
df.loc[meas_set != "full", body] = np.nan
# ovary/testis structurally absent in the youngest larvae
early = df["lifestage"].isin(["L1 (newly hatched)", "L1", "L2"])
df.loc[early, ["ov_ts", "ov_ts_pct"]] = np.nan

# round like a real spreadsheet
len_cols = ["wb_length", "ant_nr", "nr_st", "ant_st", "st", "intestine", "ov_ts", "rt_cl", "rest"]
df[len_cols] = df[len_cols].round(1)
pct_cols = [c for c in df.columns if c.endswith("_pct")]
df[pct_cols] = df[pct_cols].round(2)

# two transcription errors (ant_st inflated by 60%) for the QC step to find
ok = np.flatnonzero(df["ant_st"].notna().to_numpy())
err_rows = ok[[6, 52]]
col = df.columns.get_loc("ant_st")
df.iloc[err_rows, col] = df.iloc[err_rows, col] * 1.6

# ------------------------------------------------------------------ messy spreadsheet
raw_label = {"L1 (newly hatched)": "L1 \u2013 newly hatched",
             "Adult female": "Adult \u2013 Female",
             "Adult male": "Adult \u2013 Male"}
df["lifestage_raw"] = df["lifestage"].map(lambda x: raw_label.get(x, x))
# two stray trailing spaces, a very common typo
for r in (59, 139):
    df.iloc[r, df.columns.get_loc("lifestage_raw")] += " "

messy_cols = ["dpi", "lifestage_raw", "sample", "host_id", "wb_length",
              "ant_nr", "ant_nr_pct", "ant_st", "ant_st_pct", "nr_st", "nr_st_pct",
              "st", "st_pct", "intestine", "intestine_pct", "ov_ts", "ov_ts_pct",
              "rt_cl", "rt_cl_pct", "rest", "rest_pct", "st_number"]
raw_headers = [
    "Timepoint (dpi)", "Lifestage", "Sample", "Host ID", "WB Length",
    "Anterior body end to NR", "% of Total \u2013 Anterior body end to NR",
    "Anterior body end to Entrance of St (or end of Os)",
    "% of Total \u2013 Anterior body end to Entrance of St (or end of Os)",
    "NR to Entrance of St (or end of Os)",
    "% of Total \u2013 NR to Entrance of St (or end of Os)",
    "St", "% of Total \u2013 St", "Int", "% of Total \u2013 Int",
    "Ov/Ts", "% of Total \u2013 Ov/Ts", "Rt/Cl", "% of Total \u2013 Rt/Cl",
    "Rest of body", "% of Total \u2013 Rest of body", "APPROX. St numbers",
]
messy = df[messy_cols].copy()
messy.columns = raw_headers
empty = pd.DataFrame(np.nan, index=range(8), columns=raw_headers)   # 8 empty rows at the bottom
messy = pd.concat([messy, empty], ignore_index=True)
messy_path = out / "trichuris_muris_landmarks_messy.csv"
messy.to_csv(messy_path, index=False, na_rep="", float_format="%g", encoding="utf-8")

# ------------------------------------------------------------------ tidy table
# Same steps as Section 3 of the tutorial, applied to the messy file as written
m = pd.read_csv(messy_path)
m = m.dropna(how="all")
m.columns = messy_cols
lab = m["lifestage_raw"].str.replace(r"\s+", " ", regex=True).str.strip()
sex = np.where(lab.str.contains("female", case=False), "Female",
      np.where(lab.str.contains("male", case=False), "Male", None))
stage = np.where(lab.str.startswith("Adult"), "Adult", lab.str.extract(r"^(L[1-4])")[0])
source = np.where(lab.str.contains("newly hatched", case=False), "hatched in vitro", "host")
tidy = pd.DataFrame({
    "sample": m["sample"], "host_id": m["host_id"], "dpi": m["dpi"],
    "lifestage": stage, "sex": sex, "source": source,
    "wb_length_um": m["wb_length"], "ant_nr_um": m["ant_nr"], "ant_st_um": m["ant_st"],
    "nr_st_um": m["nr_st"], "st_um": m["st"], "intestine_um": m["intestine"],
    "ov_ts_um": m["ov_ts"], "rt_cl_um": m["rt_cl"], "rest_um": m["rest"],
    "st_number": m["st_number"],
})
tidy_path = out / "trichuris_muris_landmarks_tidy.csv"
tidy.to_csv(tidy_path, index=False, na_rep="", float_format="%g", encoding="utf-8")
print("wrote", messy_path.name, messy.shape, "and", tidy_path.name, tidy.shape)
