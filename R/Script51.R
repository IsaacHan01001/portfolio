# Variability of poll results over time

one_pollster <- polls_us_election_2016 %>% 
  filter(pollster == "Ipsos", state == "U.S.") %>% 
  mutate(spread = rawpoll_clinton/100 - rawpoll_trump/100)
se <- one_pollster %>% 
  summarize(empirical = sd(spread),
            theoretical = 2*sqrt(mean(spread)*(1-mean(spread))/min(samplesize)))
se

one_pollster %>% ggplot(aes(spread)) +
  geom_histogram(binwidth = 0.01, color = 'black')


# Peak and Trend for pollster ---------------------------------------------

polls_us_election_2016 %>% 
  filter(state == 'U.S.', enddate >= '2016-07-01') %>% 
  group_by(pollster) %>% 
  filter(n()>-10) %>% 
  ungroup() %>% 
  mutate(spread = rawpoll_clinton/100 - rawpoll_trump/100) %>% 
  ggplot(aes(enddate, spread))+
  geom_smooth(method = 'loess', span = 0.1)+
  geom_point(aes(color= pollster),show.legend=FALSE, alpha = 0.6)


# Variability Across time -------------------------------------------------

polls_us_election_2016 %>% 
  filter(state == 'U.S.', enddate >= '2016-07-01') %>% 
  select(enddate, pollster, rawpoll_clinton, rawpoll_trump) %>% 
  rename(Clinton = rawpoll_clinton, Trump = rawpoll_trump) %>% 
  gather(candidate, percentage, -enddate, -pollster) %>% 
  mutate(candidate = factor(candidate, levels = c("Trump", "Clinton"))) %>% 
  group_by(pollster) %>% 
  filter(n()>10) %>% 
  ungroup() %>% 
  ggplot(aes(enddate, percentage, color = candidate))+
  geom_point(show.legend=FALSE, alpha =0.4) +
  geom_smooth(method = 'loess', span = 0.15)+
  scale_y_continuous(limits = c(30,50))


# t-distribution ----------------------------------------------------------

#z <- qt(0.975, nrow(one_poll_per_pollster - 1)
