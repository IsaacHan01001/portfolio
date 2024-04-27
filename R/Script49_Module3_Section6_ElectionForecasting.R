library(tidyverse)
library(dslabs)
polls <- polls_us_election_2016 %>% 
  filter(state == "U.S.", enddate >= "2016-10-31",
         (grade %in% c("A+","A","A-","B+") | is.na(grade))) %>% 
  mutate(spread = rawpoll_clinton/100 - rawpoll_trump/100)

one_poll_per_pollster <- polls %>% group_by(pollster) %>% 
  filter(enddate == max(enddate)) %>% 
  ungroup()

results <- one_poll_per_pollster %>% 
  summarize(avg = mean(spread), se = sd(spread)/sqrt(length(spread))) %>% 
  mutate(start = avg - 1.96*se, end = avg +1.96*se)

mu <- 0
tau <- 0.035
sigma <- results$se
Y <- results$avg
B <- sigma^2 / (sigma^2 + tau^2)

posterior_mean <- B*mu + (1-B)*Y
posterior_se <- sqrt(1/(1/sigma^2 +1/tau^2))

posterior_mean
posterior_se

posterior_mean + c(-1.96,1.96)*posterior_se

1- pnorm(0, posterior_mean, posterior_se)


# Mathematical Representation ---------------------------------------------

J <- 6
N <- 2000
d <- 0.021
p <- (d + 1)/2
x <-  d + rnorm(J,0,2*sqrt(p*(1-p)/N))

I <- 5
J <- 6
N <- 2000
X <- sapply(1:I, function(i){
  d + rnorm(J,0, 2*sqrt(p*(1-p)/N))
})



# pollster effects --------------------------------------------------------

library(ggplot2)
library(dslabs)
library(dplyr)
library(ggthemes)
ggthemes::theme_economist()
I <- 5
J <- 6
N <- 2000
d <- 0.021
p <- (d + 1)/2
H <- rnorm(I, 0, 0.025)
x <- sapply(1:I, function(i){
  d + H[i] + rnorm(J, 0, 2*sqrt(p*(1-p)/N))
})

x_spread <- data.frame(x) %>% pivot_longer(x, cols=X1:X5, names_to = "pollster",
                                           values_to = "Spread")
x_spread %>% ggplot(aes(pollster,Spread,col=pollster))+
  geom_point() +
  scale_color_manual(values=c('darkorange','purple','cyan4','red','black'))+
  labs(x="pollster",y="spread")+
  theme_solarized()



# General Biased Variability ----------------------------------------------

my <- 0
tau <- 0.035
sigma <- sqrt(results$se^2 + 0.025^2)
T <- results$avg
B <-  sigma^2 /(sigma^2 + tau^2)

posterior_mean <- B*mu + (1-B)*Y
posterior_se <- sqrt(1/(1/sigma^2 +1/tau^2))

1-pnorm(0,posterior_mean,posterior_se)
