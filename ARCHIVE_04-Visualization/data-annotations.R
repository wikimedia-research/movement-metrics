annotations <- metrics |>
  select(month) |>
  mutate(
    curr_offset = (month %in% (current_month - years(0:4))),
    prev_offset = (month %in% ((current_month - months(1)) - years(0:4)))
  ) |>
  filter(curr_offset | prev_offset) |>
  mutate(year = year(month)) |>
  inner_join(metrics, by = "month") |>
  group_by(year) |>
  summarize(
    from = interactions_corrected[prev_offset],
    to = interactions_corrected[curr_offset],
    # The change from 2021-06 to 2021-07 (for example):
    delta = to - from,
    direction = factor(delta > 0, c(TRUE, FALSE), c("up", "down"))
  ) |>
  mutate(
    month = ymd(sprintf("%i-%02.0f-01", year, month(current_month))),
    prev_month = month - months(1)
  )

# Adding new annotations per suggestion from Margeigh to highlight 2022 vs 2019
hightlight_annotations <- metrics %>%
  mutate(
    hightlight_month = (month == current_month | month == current_month - years(3))
  ) %>%
  filter(hightlight_month) %>%
  select(month,interactions_corrected)
