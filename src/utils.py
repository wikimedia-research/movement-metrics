from numbers import Number
from pathlib import Path
from math import floor
import numpy as np
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
    
def subtract_year(period):
    # As of Oct 2023, Pandas doesn't have a way to subtract
    # a year from an arbitrary period (we want to support both months
    # and quarters), so we have to cast to a timestamp, subtract,
    # and cast back to a period
    freq = period.freqstr
    year_ago = period.to_timestamp() - pd.DateOffset(years=1)
    return pd.Period(year_ago, freq=freq)

def calc_rpt(metric, reporting_period):
    """
    * metric: a Pandas time series giving the values of a metric
    * reporting_period: a Pandas period object indicating the
      period we want to report about.
      
    Returns a Pandas series containing measurements of the metric (currently,
    the value during the reporting period, the year-over-year change, and a naive
    forecast for the next period.
    """
    # Use get rather than direct indexing so that missing data results in NaNs rather
    # than errors. We want NaNs, not nulls, so that math on them results in NaNs rather
    # than errors.
    value = metric.get(reporting_period, np.nan)

    year_ago = subtract_year(reporting_period)
    year_ago_value = metric.get(year_ago, np.nan)
    
    period_after_year_ago = year_ago + 1
    period_after_year_ago_value = metric.get(period_after_year_ago, np.nan)
    
    if year_ago_value != 0:
        year_over_year_change = (value / year_ago_value) - 1
        naive_forecast = period_after_year_ago_value / year_ago_value * value
    else:
        year_over_year_change = np.nan
        naive_forecast = np.nan
    
    return pd.Series({
        "value": value,
        "year_over_year_change": year_over_year_change,
        "naive_forecast": naive_forecast
    })


def format_number(x):
    if isinstance(x, Number) and not pd.isnull(x):
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


def format_report(df, metrics_type, reporting_period):
    """
    * df: a Pandas data frame (intended to be the output of applying calc_rpt to 
      a data frame of metrics)
    * metrics_type: a string identifying the type of metrics in the report
      (e.g. "core", "essential"). Used to add a table header.
    * reporting_period: a Pandas period identifying the period the report is 
      about. Also used in the table header
      
    Returns a formatted and styled data frame useful for
    human reading
    """
    header = f"{reporting_period} {metrics_type} metrics"
    
    new_columns= pd.MultiIndex.from_product([[header], df.columns])
    df.columns = new_columns
    
    df = (
        df
        .applymap(format_number) # changed to work with pandas series
        .fillna("–")
        .style
        .set_table_styles([{
            "selector": "th.col_heading.level0",
            "props": "font-size: 1.5em; text-align: center; font-weight: bold;"
        }])
    )
    
    return df

