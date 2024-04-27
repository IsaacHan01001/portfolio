# beads <- rep(c("red","blue"),times=c(2,3))
# x <- ifelse(sample(beads,1) == "blue",1,0)
# 
# ifelse(sample(beads,1) == "blue",1,0)


color <- rep(c('red','blue','green'),times = c(18,18,2))

n <- 1000
B <- 10000
S <- replicate(B,{
  X <- sample(c(-1,1),n,replace=TRUE,prob = c(9/19,10/19))
  sum(X)
})
mean(S<0)
mean(S)
sd(S)
# x <- sample(ifelse(color=="red",-1,1),n,replace=TRUE)
# x[1:10]


# Plotting ----------------------------------------------------------------

library(tidyverse)
p <- seq(min(S),max(S),length=100)
normal_density <- data.frame(p=p, f=dnorm(p,mean(S),sd(S)))


data.frame(S=S) %>% ggplot(aes(S,after_stat))+
  geom_histogram(col='black',binwidth=10)+
  ylab("Probability")+
  geom_line(data=normal_density,mapping=aes(p,f),col='blue')


# Central Limit Theorem ---------------------------------------------------

B <- 10^6
X <- sample(c(-1,1),B,replace=TRUE,prob=c(9/19,10/19))
mean(X)

X <- sample(c(1,-1),prob = c(1/2,1/2),1)
X
a

# Quiz --------------------------------------------------------------------

avg<- (-0.25*4/5+1/5)*44
sigma <-1.25*sqrt(4/5*1/5)*sqrt(44)
avg
1-pnorm(8,avg,sigma)


# quiz 1f -----------------------------------------------------------------

set.seed(21, sample.kind = "Rounding")

B <- replicate(10000, {
  sum(sample(c(-0.25,1),prob = c(4/5,1/5),44,replace=TRUE))
})
sum(B>=8)/length(B)

p <- seq(0.25,0.95,0.05)
avg = p*44
sigma = sqrt(p*(1-p))*sqrt(44)
which.max((1-pnorm(35,avg,sigma))>0.8)
p[13]

# Question 3:Betting on Roulette ------------------------------------------

odd_win <- 5/38
odd_lose <- 1-odd_win
E_x <- 6*odd_win-1*odd_lose
SE_x <- 7*sqrt(odd_lose*odd_win)
E_x*500
SE_x*sqrt(500)

pnorm(0,500*E_x,SE_x*sqrt(500))
1000*(20-18)/38
sqrt(500)*7*sqrt(odd_lose*odd_win)

E_x
SE_x/sqrt(500)

