# Source: https://gitlab.wikimedia.org/bearloga/pageview-2021-dataloss-estimation

host_proportions <- function(dataloss_data) {
    dataloss_data %>%
        filter(day >= "2022-01-28") %>%
        group_by(day, host) %>%
        summarize(total_views = sum(total_views), .groups = "drop_last") %>%
        mutate(prop = total_views / sum(total_views)) %>%
        ungroup
}

loss_boundaries <- function(dataloss_data) {

    host_props <- host_proportions(dataloss_data)

    # Loss 1 (2021-06-04 -- 2021-11-03): cp1087 only
    loss_1 <- host_props %>%
        filter(host == "cp1087") %>%
        summarize(
            lower = min(prop),
            middle = median(prop),
            upper = max(prop)
        )

    # Loss 2 (2021-11-04 -- 2021-01-27): cp1087, cp4035, cp4036
    loss_2 <- host_props %>%
        mutate(inv_prop = 1 - prop) %>%
        filter(host == "Other") %>%
        summarize(
            lower = min(inv_prop),
            middle = median(inv_prop),
            upper = max(inv_prop)
        )

    return(list(
        loss1 = loss_1,
        loss2 = loss_2,
        none = c(lower = 0, middle = 0, upper = 0)
    ))
}