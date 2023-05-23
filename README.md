This repo contains all the code needed to calculate the monthly Wikimedia movement metrics related to content and contributors. It has three main dependencies:
* This code is designed to run on one of the [Jupyter Notebook](https://wikitech.wikimedia.org/wiki/SWAP) servers and will not work elsewhere.
* The contributors-related metrics are calculated from the [mediawiki_history dataset](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history). 
* The content-related metrics are calculated from the [AQS](https://wikitech.wikimedia.org/wiki/Analytics/Systems/AQS) [API](https://wikimedia.org/api).

For more details about our monthly reporting process, see [mw:Product Analytics/Movement metrics](https://www.mediawiki.org/wiki/Product_Analytics/Movement_metrics).

For a full list of metric definitions, see [mw:Wikimedia Product/Data glossary](https://www.mediawiki.org/wiki/Wikimedia_Product/Data_glossary).

# Usage
1. Clone this onto a) your [JupyterHub](https://wikitech.wikimedia.org/wiki/SWAP) server and b) to your local machine. 
2. run notebook 01-run.ipynb
    
    * [02a-calculation.ipynb](02a-calculation.ipynb), calculates the metrics (some of them using the editor-month and new editor tables) and inserts them into metrics.tsv.
    * [02b-diversity-calculation.ipynb](02b-diversity-calculation.ipynb), calculates the diversity metrics (some of them using the editor-month and new editor tables) and inserts them into diversity_metrics.tsv.
    * [03-report.ipynb](03-report.ipynb), simple transformations on the metrics and produces the table of values needed for the final report; previously this also produced a graph of each metric. This graph code needs to be updated before it can be used again.
    
    Note: We have automated the two notebooks numbered 01 which run in the first week of every month to load needed data into needed tables:
    * [ARCHIVE_01a-editor-month-table.ipynb](ARCHIVE_01a-editor-month-table.ipynb): creates or updates an intermediate editor-month table in the wmf_product Hive database.
    * [ARCHIVE_01b-new-editor-table.ipynb](ARCHIVE_01b-new-editor-table.ipynb): creates or updates an intermediate table of new editors in the wmf_product Hive database
    
3. once you've run 01-run.ipynb, commit and push the notebook changes to the Github repo to keep 'origin' updated
4. open your local version of this repo (which includes the json key) and git pull changes
5. fronm your local, run notebook 03b
6. commit and push the notebook changes to the Github repo to keep 'origin' updated   
    

7. Do any analysis you need to understand major trends (drawing on the analysis notes in past months' slides if needed). The [analysis folder](analysis) has a variety of notebook you could reuse; if you do new analysis, considering keeping it in an existing or new notebook in this folder, so it can be reused in the future.

    Note: The following visualization notebooks have been archived until updates are made to update the code:
    * [ARCHIVE_Visualiaztion.ipynb](ARCHIVE_Visualzation.ipynb) using R kernel, provides YoY charts for metrics in the metrics deck. This code needs to be updated before it can be used agian.