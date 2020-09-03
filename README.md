This repo contains all the code needed to calculate the monthly Wikimedia movement metrics related to content and contributors. It has three main dependencies:
* This code is designed to run on one of the [SWAP](https://wikitech.wikimedia.org/wiki/SWAP) servers and will not work elsewhere.
* The contributors-related metrics are calculated from the [mediawiki_history dataset](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history). 
* The content-related metrics are calculated from the [AQS](https://wikitech.wikimedia.org/wiki/Analytics/Systems/AQS) [API](https://wikimedia.org/api).

For more details about our monthly reporting process, see [mw:Product Analytics/Movement metrics](https://www.mediawiki.org/wiki/Product_Analytics/Movement_metrics).

For a full list of metric definitions, see [mw:Wikimedia Product/Data dictionary](https://www.mediawiki.org/wiki/Wikimedia_Product/Data_dictionary).

# Usage
1. Clone this onto one of the [SWAP](https://wikitech.wikimedia.org/wiki/SWAP) hosts.
1. In any order, run the two notebooks numbered 01
    * [01a-editor-month-table.ipynb](01a-editor-month-table.ipynb): creates or updates an intermediate editor-month table in the neilpquinn Hive database.
    * [01b-new-editor-table.ipynb](01b-new-editor-table.ipynb): creates or updates an intermediate table of new editors in the neilpquinn Hive database.
1. In any order, run the two notebooks numbered 02
    * [02a-calculation.ipynb](02a-calculation.ipynb), which actually calculates the metrics (some of them using the editor-month and new editor tables calculated in the previous step) and inserts them into metrics.tsv.
    * [02b-diversity-calculation.ipynb](02b-diversity-calculation.ipynb), which calculates the diversity metrics (some of them using the editor-month and new editor tables calculated in the previous step) and inserts them into diversity_metrics.tsv.
1. Run the notebook [03-report.ipynb](03-report.ipynb), which does a few simple transformations on the metrics and produces the table of values needed for the final report, as well as a graph of each metric.
1. Run the notebook [04-Visualiaztion.ipynb](03-Visualzation.ipynb), which provides YoY charts for metrics in the metrics deck.
1. Do any analysis you need to understand major trends (drawing on the analysis notes in past months' slides if needed). The [analysis folder](analysis) has a variety of notebook you could reuse; if you do new analysis, considering keeping it in an existing or new notebook in this folder, so it can be reused in the future.
