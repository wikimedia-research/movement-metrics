# Readers-core-metrics

This repo contains all the code needed to calculate the monthly Wikimedia movement metrics related to reading activity including page interactions (pageviews and seen previews) and unique devices. Dependencies include:

* This code is designed to run on one of the [Jupyter Notebook](https://wikitech.wikimedia.org/wiki/SWAP) servers and will not work elsewhere.
* The Metics are calculated from the following sources:  
  + previews: [virtualpageview_hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Virtualpageview_hourly)
  + pageviews: [pageview hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageview_hourly)
  + unique devices:  [unique_devices_per_project_family_monthly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Unique_Devices)

## Usage
1. Clone this onto your [JupyterHub](https://wikitech.wikimedia.org/wiki/SWAP) server. 
2. In any order, run the two notebooks numbered 02
    * [02a-calculation.ipynb](02a-calculation.ipynb), which actually calculates the metrics and inserts them into metrics.tsv.
    * [02b-diversity-calculation.ipynb](02b-diversity-calculation.ipynb), which calculates the diversity metrics and inserts them into diversity_metrics.tsv.
3. Run the notebook [03-report.ipynb](03-report.ipynb), which does a few simple transformations on the metrics and produces the table of values needed for the final report, as well as a graph of each metric.
4. Run the scripts in [04-Visualization](04-Visualization) using R kernel or Rstudio, which provides trend charts for metrics in the Key Product metrics deck.
5. Note: We have automated the two notebooks numbered 01 which runs in the first week of every month 
    * [01a-update_pageviews_table.ipynb](https://github.com/wikimedia-research/Readers-movement-metrics/blob/main/01a-update_pageviews_table.ipynb): creates or updates an intermediate pageviews_corrected table in the wmf_product Hive database.
    * [01b-update_diversity_table.ipynb](https://github.com/wikimedia-research/Readers-movement-metrics/blob/main/01b-update_diversity_table.ipynb): creates or updates an intermediate global_markets_pageviews tables in the wmf_product Hive database.
6. Do any other analysis needed to understand major trends. 

## Data Definitions

Current definitions of these core metrics are documented in the [Wikimedia Audience Data Dictionary page](https://www.mediawiki.org/wiki/Wikimedia_Product/Data_dictionary#Core_metrics).
