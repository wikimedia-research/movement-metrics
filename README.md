# Readers-core-metrics

This repo contains all the code needed to calculate the monthly Wikimedia movement metrics related to reading activity including page interactions (pageviews and seen previews) and unique devices. Dependencies include:

* This code is designed to run on one of the [SWAP](https://wikitech.wikimedia.org/wiki/SWAP) servers and will not work elsewhere.
* The Metics are calculated from the following sources:  
  + previews: [virtualpageview_hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Virtualpageview_hourly)
  + pageviews: [pageview hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageview_hourly), 
  + unique devices:  [unique_devices_per_project_family_monthly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Unique_Devices)

## File Overview
- Files in the `queries` directory includes the queries used for fetching the data.
- Files in the `figures` directory includes the graphs produced during the analysis
- `01_interactions_metrics.ipynb` contains the analysis for calculating monthly interactions (pageviews and seen previews).
- `02-unique_devices.ipynb` contains the analysis for calculating the total unique devices each month.
- `03_diversity_metrics.ipynb` contains the analysis for calculating interactions for identified global south wikis and mobile-heavy wikis. 

## Usage
1. Clone this onto one of the [SWAP](https://wikitech.wikimedia.org/wiki/SWAP) hosts. 
2. Run the notebook `01_interactions_metrics.ipynb` to caluclate overall monthly interactios (pageviews and seen previews)
3. Run the notebook ``02-unique_devices.ipynb` to calculate total unqiue devices each month.
4. Run the notebook `03_diversity_metrics.ipynb` to calculate interactions for identified global south wikis and mobile-heavy wikis. 
5. Do any other analysis needed to understand major trends. 

## Data Definitions

Current definitions of these core metrics are documented in the [Wikimedia Audience Data Dictionary page](https://www.mediawiki.org/wiki/Wikimedia_Product/Data_dictionary#Core_metrics).
