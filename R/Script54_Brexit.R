library(dslabs)
library(tidyverse)
library(dplyr)
options(digits = 3)
data("brexit_polls")

p <- 0.481
d <- 2*p -1


# start -------------------------------------------------------------------

N <- 1500
N*p
sqrt(N*p*(1-p))
2*sqrt(p*(1-p)/N)

head(brexit_polls)

brexit_polls <- brexit_polls %>% 
  mutate(x_hat = (spread + 1)/2)

mean(brexit_polls$spread)
brexit_polls %>% summarize(sd(spread))

mean(brexit_polls$x_hat)
brexit_polls %>% summarize(sd(x_hat))


# First poll --------------------------------------------------------------

First_poll <- brexit_polls[1,]
First_poll
First_poll %>% summarize(qnorm(0.025,x_hat,sqrt(x_hat*(1-x_hat)/samplesize)))
First_poll %>% summarize(qnorm(0.975,x_hat,sqrt(x_hat*(1-x_hat)/samplesize)))


# Brexit part2 ------------------------------------------------------------

data("brexit_polls")
brexit_polls <- brexit_polls %>% 
  mutate(x_hat = (spread + 1)/2)
p <- 0.481

june_polls <- brexit_polls %>% filter(enddate >="2016-06-01")
june_polls <- june_polls %>% mutate(se_x_hat = 2*sqrt(x_hat*(1-x_hat)/samplesize),
                                    lower = spread + qnorm(0.025)*se_x_hat,
                                    upper = spread + qnorm(0.975)*se_x_hat,
)

nrow(june_polls)
sum(june_polls$lower<=0 & 0<=june_polls$upper)

june_polls %>% summarize(sum(lower<=d & d<=upper))

# Group by pollsters ------------------------------------------------------

head(june_polls)
k <- june_polls %>% group_by(pollster) %>% summarize(hit_rate = sum(lower<=d & d<=upper)/n(),n =n(), right = hit_rate*n) %>% 
  arrange(-hit_rate)
k

head(june_polls)
june_polls %>% group_by(poll_type) %>% ggplot(aes(poll_type,spread)) + geom_boxplot()

k <- june_polls %>% group_by(poll_type) %>% summarize(N = sum(samplesize),spread = sum(spread*samplesize)/N,
                                                 p_hat = (spread +1)/2)
k

a1 <- k %>% summarize(spread[1] + qnorm(0.025)*2*sqrt(p_hat[1]*(1-p_hat[1])/N[1]))
a2 <- k %>% summarize(spread[1] + qnorm(0.975)*2*sqrt(p_hat[1]*(1-p_hat[1])/N[1]))

b1 <- k %>% summarize(spread[2] + qnorm(0.025)*2*sqrt(p_hat[2]*(1-p_hat[2])/N[2]))
b2 <- k %>% summarize(spread[2] + qnorm(0.975)*2*sqrt(p_hat[2]*(1-p_hat[2])/N[2]))

# Part3 -------------------------------------------------------------------

data("brexit_polls")
head(brexit_polls)
brexit_polls <- brexit_polls %>% 
  mutate(x_hat = (spread + 1)/2)
p <- 0.481

brexit_hit <- brexit_polls %>% 
  mutate(p_hat = (spread + 1)/2,
         se_spread = 2*sqrt(p_hat*(1-p_hat)/samplesize),
         spread_lower = spread - qnorm(.975)*se_spread,
         spread_upper = spread + qnorm(.975)*se_spread,
         hit = spread_lower < -0.038 & spread_upper > -0.038) %>% 
  select(poll_type,hit)

mat <- brexit_hit %>% group_by(poll_type,hit) %>% summarize(n = n()) %>% spread(poll_type,n)
mat %>% select(-hit) %>% chisq.test()

(48/37)
(10/32)

(48/37)/(10/32)

head(brexit_polls)

brexit_polls %>% ggplot(aes(x=enddate,y=spread,col=poll_type)) +
  geom_point()+
  geom_smooth(method='loess',span = 0.4)+
  geom_hline(yintercept = -0.038)

# Brexit long -------------------------------------------------------------

brexit_long <- brexit_polls %>% 
  gather(vote, proportion, "remain":"undecided") %>% 
  mutate(vote = factor(vote))
head(brexit_long)
head(brexit_polls)


brexit_long %>% ggplot(aes(x=enddate,y=proportion,col=vote))+
  geom_point()+
  geom_smooth(method = 'loess',span = 0.3)
