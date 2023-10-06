from numbers import Number
from pathlib import Path

import pandas as pd

from wmfdata.utils import pct_str, sig_figs

def load_metric_file(filename):
    return (
        pd
        .read_csv(filename, sep="\t", parse_dates=["month"], index_col="month")
        .to_period()
    )

def load_all_metric_files():
    metrics_dir = Path("metrics")

    dfs = []

    for file in metrics_dir.iterdir():
        if file.suffix == ".tsv":
            df = load_metric_file(file)
            dfs.append(df)
            
    metrics = dfs[0].join(dfs[1:], how="outer", sort=True)

    return metrics

def fmt_num(x):
    if isinstance(x, Number) and not pd.isnull(x):
        x = sig_figs(x, 3)
        M = 1_000_000
        G = 1_000_000_000
        
        if x < 5:
            return pct_str(x)
        elif x < M:
            return "{:,.0f}".format(x)
        elif x < G:
            x_in_M = sig_figs(x / M, 3)
            return f"{x_in_M} M"
        else:
            x_in_G = sig_figs(x / G, 3)
            # I would like to use G here, but in my experience, people don't
            # necessarily understand what it means but do understand B for "billion".
            return f"{x_in_G} B"
    else:
        return x
    
def subtract_year(period):
    # As of Oct 2023, Pandas doesn't have a way to subtract
    # a year from an arbitrary period (we want to support both months
    # and quarters), so we have to cast to a timestamp, subtract,
    # and cast back to a period
    freq = period.freqstr
    year_ago = period.to_timestamp() - pd.DateOffset(years=1)
    return pd.Period(year_ago, freq=freq)

def calc_rpt(ser):   
    latest = ser.index[-1]
    latest_value = ser[latest]
    # previous_period = latest_period - 1
    # previous_value = ser[previous_period]
    
    year_ago = subtract_year(latest)
    year_ago_value = ser[year_ago]
    period_after_year_ago = year_ago + 1
    period_after_year_ago_value = ser[period_after_year_ago]
    
    year_over_year_change = (latest_value / year_ago_value) - 1

    naive_forecast = period_after_year_ago_value / year_ago_value * latest_value
    
    res = [latest_value, year_over_year_change, naive_forecast]
    return pd.Series(
        [fmt_num(n) for n in res],
        index=[
            "value",
            "change_over_past_year",
            "naive_forecast_for_next_period"
        ]
    )
