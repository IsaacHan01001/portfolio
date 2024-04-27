library(dslabs)
library(tidyverse)
data(nhtemp)
data.frame(year=as.numeric(time(nhtemp)),temperature=as.numeric(nhtemp)) %>% 
  ggplot(aes(year, temperature))+
  geom_point()+
  geom_smooth()+
  ggtitle("Average Yearly temperatures in New Haven")


# Monte Carlo Simulation --------------------------------------------------

p <- 0.45
N <- 1000
X <- sample(c(0,1),size=N, replace = TRUE, prob=c(1-p,p))
X_hat <- mean(X)
SE_hat <- sqrt(X_hat*(1-X_hat)/N)
c(X_hat-2*SE_hat,X_hat+2*SE_hat)

# Solving with qnorm ------------------------------------------------------

z <- qnorm(0.995)
pnorm(qnorm(0.995))
pnorm(qnorm(1-0.995))
pnorm(z)-pnorm(-z)

# monte carlo for confidence intervals ------------------------------------

B <- 10^4
inside <- replicate(B,{
  x <- sample(c(0,1),size=N,replace=TRUE,prob=c(1-p,p))
  x_hat <- mean(x)
  se_hat <- sqrt(x_hat*(1-x_hat)/N)
  between(p,x_hat-2*se_hat,x_hat+2*se_hat)
})
mean(inside)

# Power -------------------------------------------------------------------

N <- 25
x_hat <- 0.48
(2*x_hat-1)+c(-2,2)*2*sqrt(x_hat*(1-x_hat)/N)
