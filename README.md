# Readers-core-metrics

This repo contains all the code needed to calculate the monthly Wikimedia movement metrics related to reading activity including page interactions (pageviews and seen previews) and unique devices. Dependencies include:

* This code is designed to run on one of the [SWAP](https://wikitech.wikimedia.org/wiki/SWAP) servers and will not work elsewhere.
* The Metics are calculated from the following sources:  
  + previews: [virtualpageview_hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Virtualpageview_hourly)
  + pageviews: [pageview hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageview_hourly), 
  + unique devices:  [unique_devices_per_project_family_monthly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Unique_Devices)

## Usage
1. Clone this onto one of the [SWAP](https://wikitech.wikimedia.org/wiki/SWAP) hosts. 
2. In any order, run the two notebooks numbered 01
   * [01a-update_pageviews_table.ipynb](01a-update_pageviews_table.ipynb): creates or updates an intermediate pageviews_corrected table in the cchen Hive database.
   * [01b-update_diversity_table.ipynb](01b-update_diversity_table.ipynb): creates or updates intermediate diversity market pageview tables in the cchen Hive database.
3. In any order, run the two notebooks numbered 02
    * [02a-calculation.ipynb](02a-calculation.ipynb), which actually calculates the metrics and inserts them into metrics.tsv.
    * [02b-diversity-calculation.ipynb](02b-diversity-calculation.ipynb), which calculates the diversity metrics and inserts them into diversity_metrics.tsv.
4. Run the notebook [03-report.ipynb](03-report.ipynb), which does a few simple transformations on the metrics and produces the table of values needed for the final report, as well as a graph of each metric.
5. Run the notebook [04-Visualiaztion.ipynb](03-Visualzation.ipynb), which provides YoY charts for metrics in the metrics deck.
6. Do any other analysis needed to understand major trends. 

## Data Definitions

Current definitions of these core metrics are documented in the [Wikimedia Audience Data Dictionary page](https://www.mediawiki.org/wiki/Wikimedia_Product/Data_dictionary#Core_metrics).
