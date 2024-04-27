library(tidyverse)
library(dslabs)
data(death_prob)
head(death_prob)
str(death_prob)

p_50_female <- death_prob %>% filter(age==50,sex=="Female") %>% pull(prob)

E_x <- -150000*p_50_female+1150*(1-p_50_female)
SE_x <- 151150*sqrt(p_50_female*(1-p_50_female))
SE_x
1000*E_x
SE_x*sqrt(1000)
pnorm(0,E_x*1000,SE_x*sqrt(1000))


p_50_male <- death_prob %>% filter(age==50,sex=="Male") %>% pull(prob)
p_50_male
price_male <- (700+150000*p_50_male)/(1-p_50_male)
E_male <- -150000*p_50_male+price_male*(1-p_50_male)


sqrt(1000)*(150000+price_male)*sqrt(p_50_male*(1-p_50_male))
pnorm(0,E_male*1000,sqrt(1000)*(150000+price_male)*sqrt(p_50_male*(1-p_50_male))
)

# Part3 -------------------------------------------------------------------

p_now <- 0.015
E_x_now <- -150000*p_now+1150*(1-p_now)
E_x_now*1000
SE_now <- 151150*sqrt(p_now*(1-p_now))
SE_now*sqrt(1000)

pnorm(-10^6,E_x_now*1000,SE_now*sqrt(1000))

p <- seq(.01,.03,.0025)
avg <- -150000*p+1150*(1-p)
se <- 151150*sqrt(p*(1-p))
which.max(pnorm(-10^6,avg*1000,se*sqrt(1000))>0.9)
p[5]

# Question4 ---------------------------------------------------------------

set.seed(25,sample.kind = "Rounding")
p_loss <- 0.015

sum(sample(c(-150000,1150),1000,prob = c(p_loss,1-p_loss),replace=TRUE))/10^6


set.seed(27,sample.kind = "Rounding")
p_loss <- 0.015
result <- replicate(10000,{
  sum(sample(c(-150000,1150),1000,prob = c(p_loss,1-p_loss),replace=TRUE))/10^6
})
mean(result < -1)
result


# Question5 ---------------------------------------------------------------

p <- 0.015
n <- 1000
l <- -150000
z <- -1.644854
z<-qnorm(0.05)
price <- 3268.0633276082395104667515616531

E_x <- l*p+price*(1-p)
E_x*1000


# Question 5d -------------------------------------------------------------

set.seed(28,sample.kind = "Rounding")
simulation <- replicate(10000,{
  sum(sample(c(l,price),1000,prob = c(p,1-p),replace=TRUE))
})

mean(simulation<0)


# -------------------------------------------------------------------------

set.seed(29,sample.kind = "Rounding")

p <- 0.015
simulation <- replicate(10000,{
  p <- p+sample(seq(-0.01,0.01,length=100),1)
  sum(sample(c(l,price),1000,prob = c(p,1-p),replace=TRUE))
})

mean(simulation < -10^6)
mean(simulation)
