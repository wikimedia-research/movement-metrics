from pathlib import Path

import pandas as pd

def load_metric_file(filename):
    return pd.read_csv(filename, sep="\t", parse_dates=["month"], index_col="month")

def load_all_metric_files():
    metrics_dir = Path("metrics")

    dfs = []

    for file in metrics_dir.iterdir():
        if file.suffix == ".tsv":
            df = load_metric_file(file)
            dfs.append(df)
            
    metrics = dfs[0].join(dfs[1:], how="outer")

    return metrics
    