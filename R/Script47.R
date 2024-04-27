d <- 0.039
Ns <- c(1298, 533, 1342, 897, 774, 254, 812, 324, 1291, 1056, 2172, 516)
p <- (d + 1)/2

confidence_intervals <- sapply(Ns, function(N) {
  x <- sample(c(0,1), size = N, replace = TRUE, prob = c(1-p, p))
  x_hat <- mean(x)
  se_hat <-  sqrt(x_hat*(1-x_hat)/N)
  2*c(x_hat, x_hat - 2*se_hat, x_hat +2*se_hat)-1
})

polls <- data.frame(poll=1:ncol(confidence_intervals), t(confidence_intervals), sample_size = Ns)
names(polls) <- c("poll", "estimate", "low", "high", "sample_size")

polls
# Poll Aggregators --------------------------------------------------------

library(dplyr)
sum(polls$sample_size)
d_hat <- polls %>% 
  summarize(avg = sum(estimate*sample_size) / sum(sample_size)) %>% 
  .$avg
p_hat <- (1+d_hat)/2
moe <- 2*1.96*sqrt(p_hat*(1-p_hat)/sum(polls$sample_size))
moe
d_hat


# polls -------------------------------------------------------------------

library(dslabs)
library(ggplot2)
polls <- polls_us_election_2016 %>% 
  filter(state == "U.S." & enddate >= "2016-10-31" & (grade %in% c("A+", "A", "A-", "B+") | is.na(grade)))
polls <- polls %>% mutate(spread = rawpoll_clinton/100 - rawpoll_trump/100)
d_hat <- polls %>% summarize(d_hat = sum(spread*samplesize)/sum(samplesize)) %>% 
  .$d_hat
p_hat <- (d_hat+1)/2
moe <- 1.96*2*sqrt(p_hat*(1-p_hat)/sum(polls$samplesize))
polls %>% ggplot(aes(spread))+
  geom_histogram(color='black',binwidth=.01)


# ----------- -------------------------------------------------------------


polls %>% group_by(pollster) %>% summarize(n())
polls %>% group_by(pollster) %>% 
  filter(n()>=6) %>% 
  ggplot(aes(pollster,spread))+
  geom_point()+
  theme(axis.text.x=element_text(angle=90, hjust=1))
polls %>% group_by(pollster) %>% 
  filter(n()>=6) %>% 
  summarize(se = 2*sqrt(p_hat*(1-p_hat)/median(samplesize)))

# ------------------ ------------------------------------------------------

one_poll_per_pollster <- polls %>% group_by(pollster) %>% 
  filter(enddate == max(enddate)) %>% 
  ungroup()
one_poll_per_pollster
sd(one_poll_per_pollster$spread)

results <- one_poll_per_pollster %>% 
  summarize(avg = mean(spread), se = sd(spread)/sqrt(length(spread))) %>% 
  mutate(start = avg-1.98*se, end = avg+1.96*se)
round(results*100,1)
