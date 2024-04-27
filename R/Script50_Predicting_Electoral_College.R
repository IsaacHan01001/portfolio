library(dslabs)
library(dplyr)
library(tidyverse)
data("polls_us_election_2016")

results <- polls_us_election_2016 %>% 
  filter(state!="U.S.", enddate >="2016-10-31",
         !grepl("CD",state),
         (grade %in% c("A+","A","A-", "B+") | is.na(grade))) %>%
  mutate(spread = rawpoll_clinton/100 - rawpoll_trump/100) %>% 
  group_by(state) %>% 
  summarize(avg = mean(spread), sd = sd(spread), n = n()) %>% 
  mutate(state = as.character(state))

  
results %>% arrange(abs(avg))


# left poll ---------------------------------------------------------------

results <- left_join(results, results_us_election_2016, by = "state")
results_us_election_2016 %>% filter(!state %in% results$state)
results <- results %>% 
  mutate(sd = ifelse(is.na(sd), median (results$sd,na.rm=TRUE),sd))


# Bayesian Calculation ----------------------------------------------------

mu <- 0
tau <- 0.02
results %>% mutate(sigma = sd/sqrt(n), B = sigma^2/(sd^2 + tau^2),
                   posterior_mean = B*mu + (1-B)*avg,
                   posterior_se <- sqrt(1/(1/ sigma^2 + 1/tau^2))) %>% 
  arrange(abs(posterior_mean))

# Monte Carlo -------------------------------------------------------------

mu <- 0
tau <- 0.02
clinton_EV <- replicate(250, {
  results %>% mutate(sigma = sd/sqrt(n),
    B = sigma^2/(sigma^2 + tau^2),
    posterior_mean <- B*mu + (1-B)*avg,
    posterior_se <- sqrt(1/(1/sigma^2 + 1/tau^2)),
    simulated_results = rnorm(length(posterior_mean), posterior_mean, posterior_se),
    clinton = ifelse(simulated_results>0, electoral_votes, 0)) %>%
    summarize(clinton = sum(clinton)) %>% 
    .$clinton + 7 ## 7 for Rhode and D.C.
})

mean(clinton_EV >269)

data.frame(clinton_EV) %>% 
  ggplot(aes(clinton_EV)) +
  geom_histogram(binwidth = 1) +
  geom_vline(xintercept = 269)


# with general bias -------------------------------------------------------

mu <- 0
tau <- 0.02
bias_sd <- 0.03
clinton_EV <- replicate(1000, {
  results %>% mutate(sigma = sqrt(sd^2/n + bias_sd^2),
                     B = sigma^2/(sigma^2 + tau^2),
                     posterior_mean <- B*mu + (1-B)*avg,
                     posterior_se <- sqrt(1/(1/sigma^2 + 1/tau^2)),
                     simulated_results = rnorm(length(posterior_mean), posterior_mean, posterior_se),
                     clinton = ifelse(simulated_results>0, electoral_votes, 0)) %>%
    summarize(clinton = sum(clinton)) %>% 
    .$clinton + 7 ## 7 for Rhode and D.C.
})

mean(clinton_EV >269)

data.frame(clinton_EV) %>% 
  ggplot(aes(clinton_EV)) +
  geom_histogram(binwidth = 1) +
  geom_vline(xintercept = 269)
