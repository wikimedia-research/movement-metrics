This repo contains all the code needed to calculate the monthly Wikimedia movement metrics. Dependencies include:

* The contributors-related metrics are calculated from the [mediawiki_history dataset](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history). 
* The content-related metrics are calculated from the [AQS](https://wikitech.wikimedia.org/wiki/Analytics/Systems/AQS) [API](https://wikimedia.org/api).
* The readers-related metrics are calculated from the following sources:  
  + previews: [virtualpageview_hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Virtualpageview_hourly)
  + pageviews: [pageview hourly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageview_hourly)
  + unique devices: [unique_devices_per_project_family_monthly](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Unique_Devices)
  
For more details about our monthly reporting process, see [mw:Product Analytics/Movement metrics](https://www.mediawiki.org/wiki/Product_Analytics/Movement_metrics).

For a full list of metric definitions, see [mw:Research and Decision Science/Data glossary](https://meta.wikimedia.org/wiki/Research_and_Decision_Science/Data_glossary).

## Setup
The calculation code is designed to run on one of the [analytics client servers](https://wikitech.wikimedia.org/wiki/Analytics/Systems/Clients) servers and will not work elsewhere.

Clone this onto your chosen [analytics client server](https://wikitech.wikimedia.org/wiki/Analytics/Systems/Clients) server. 

Install the dependencies by running the following command:
```
conda env update -f env.yaml
```

## Use
1. Run the notebook [01-calculate.ipynb](01-calculate.ipynb), which actually calculates the metrics and inserts them into several files in the `metrics` directory.
2. Run the notebook [02-report.ipynb](02-report.ipynb), which does a few simple transformations on the metrics and produces the table of values needed for the final report, as well as a graph of each metric.
3. Commit and push the resulting changes to the GitHub repo with the commit message "Update MONTH YEAR metrics". 
4. Clone this repo to your local machine (or pull the new changes if it is already cloned).
5. Ensure that you have the JSON key containing the Google service account credentials in the main directory of the repo. (There are two service accounts and either will work, if you point the code to the file.)
5. Run the notebook [03-update-google-sheets.ipynb](03-update-google-sheets.ipynb).
