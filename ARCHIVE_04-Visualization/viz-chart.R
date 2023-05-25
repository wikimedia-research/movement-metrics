library(scales)
library(hrbrthemes)

p <- metrics |>
  filter(period != "during dataloss") |>
  ggplot() +
  geom_point(
    aes(x = month, y = interactions_corrected),
    data = hightlight_annotations,
    # modified per suggestion from Margeigh to highlight 2022 vs 2019
    shape = 21, stroke = 1, size = 20,
    color = wmf_colors$Yellow50, 
    #fill = wmf_colors$Yellow90,
    # removing per suggestion from Margeigh
    alpha = 0.5
  ) +
  ## Undercounted due to data loss:
  geom_line(
    aes(x = month, y = interactions),
    data = metrics |> filter(dataloss),
    color = wmf_colors$Accent50,
    linetype = "33",
  ) +
  geom_line(
    aes(x = month, y = interactions, group = period),
    color = wmf_colors$Accent30
  ) +
  ## Corrected estimate:
  geom_line(
    aes(x = month, y = interactions_corrected),
    data = metrics |> filter(dataloss),
    color = wmf_colors$Accent30,
    linetype = "92",
  ) +
  geom_point(
    aes(x = month, y = to),
    size = 2, # default 1.5
    color = wmf_colors$Accent30,
    data = annotations
  ) +
  scale_y_continuous(
    name = NULL,
    labels = label_number(scale = 1e-9, suffix = " B", accuracy = 1),
    breaks = seq(16e9, 23e9, 1e9),
    limits = c(16e9, 23e9)
  ) +
  scale_x_date(
    name = NULL,
    breaks = annotations$month,
    date_minor_breaks = "1 month",
    date_labels = "%B\n%Y"
  ) +
  theme_ipsum_rc(grid = "Yy", base_family = "Arial") +
  theme(
    plot.background = element_rect(fill = "white", color = "white"),
    panel.grid.major.y = element_line(color = wmf_colors$Base70),
    panel.grid.minor.y = element_line(color = wmf_colors$Base80),
    axis.text.x = element_text(size = 14),
    axis.text.y = element_text(size = 14)
  ) 
  
p + ggtitle("Content Interactions")
