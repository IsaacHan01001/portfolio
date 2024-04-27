library(tidyverse)
n <- 1000
loss_per_foreclosure <- -200000
p <- 0.02



# Monte Carlo Simulation --------------------------------------------------


B <- 10000
losses <- replicate(B,{
  defaults <- sample(c(0,1),n,prob=c(1-p,p),replace=TRUE)
  losses <-  sum(defaults*loss_per_foreclosure)
})
data.frame(losses_in_millions = losses/10^6) %>% ggplot(aes(losses_in_millions))+
  geom_histogram(binwidth=0.6,col='black')

x_break_even<- -loss_per_foreclosure*p/(1-p)


# Big Short ---------------------------------------------------------------

p <- 0.04
l <- -200000
r <- 0.05
x <- r*180000
loss_per_foreclosure*p+x*(1-p)


# -------n------------------------------------------------------------------

z <- qnorm(0.01)
n <- ceiling((z^2*(x-l)^2*p*(1-p))/(l*p+x*(1-p))^2)
n


# MonteCarlo --------------------------------------------------------------

p <- 0.04
x <- 0.05*180000
profit <- replicate(B,{
  draws <- sample(c(x,loss_per_foreclosure),n,prob=c(1-p,p),replace=TRUE)
  sum(draws)
})
mean(profit<0)


# Non-independence --------------------------------------------------------

p <- 0.04
x <- 0.05*180000
profit <- replicate(B,{
  new_p <- 0.04+sample(seq(-0.01,0.01,length=100),1)
  draws <- sample(c(x,loss_per_foreclosure),n,prob = c(1-new_p,new_p),replace=TRUE)
  sum(draws)
})
profit
mean(profit)
mean(profit<0)
profit
mean(profit < -10000000)
profit

data.frame(profit=profit) %>% ggplot(aes(profit,after_stat(count))) +
  geom_histogram(col='black')
