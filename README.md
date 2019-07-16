This repo contains all the code needed to calculate the monthly Wikimedia movement metrics related to content and contributors. It has three main dependencies:
* This code is designed to run on one of the [SWAP](https://wikitech.wikimedia.org/wiki/SWAP) servers and will not work elsewhere.
* The contributors-related metrics are calculated from the [mediawiki_history dataset](https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Edits/Mediawiki_history)
* The content-related metrics are calculated from the [AQS](https://wikitech.wikimedia.org/wiki/Analytics/Systems/AQS) [API](https://wikimedia.org/api).

For more details about our monthly reporting process, see [mw:Product Analytics/Movement metrics](https://www.mediawiki.org/wiki/Product_Analytics/Movement_metrics).

For a full list of metric definitions, see [mw:Wikimedia Product/Data dictionary](https://www.mediawiki.org/wiki/Wikimedia_Product/Data_dictionary).
