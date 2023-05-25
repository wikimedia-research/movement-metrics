library(here)
library(tidyverse)
library(lubridate)

metrics <- here("04-Visualization/corrected_metrics.csv") |>
  read_csv(show_col_types = FALSE) |>
  janitor::clean_names() |>
  arrange(month) |>
  filter(month >= "2018-05-01")

current_month <- max(metrics$month)

metrics <- metrics |>
  mutate(
    dataloss = (pageview_multiplier > 1.0) |
      month %in% (
        metrics |>
          filter(pageview_multiplier > 1.0) |>
          pull(month) |>
          range() |>
          (\(x) x + months(c(-1, 1)))()
      ),
    period = case_when(
      month < "2021-06-01" ~ "before dataloss",
      month >= "2021-06-01" & month < "2022-02-01" ~ "during dataloss",
      month >= "2022-02-01" ~ "after dataloss"
    )
  )
