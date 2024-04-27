library(tidyverse)

set.seed(16, sample.kind = "Rounding")

act_scored <- rnorm(10000,20.9,5.7)
mean(act_scored)
sd(act_scored)

act_scored[act_scored>=36]
sum(act_scored>=36)

length(act_scored)
sum(act_scored<=10)/length(act_scored)
x <- 1:36
f_x <- dnorm(x,20.9,5.7)
plot(x,f_x)


# Part2 -------------------------------------------------------------------

z_score <- (act_scored-mean(act_scored))/sd(act_scored)
sum(z_score>2)/length(z_score)

2*sd(act_scored)+mean(act_scored)
qnorm(0.975,mean(act_scored),sd(act_scored))

# Part 3 ------------------------------------------------------------------

f<-function(x) sum(act_scored<=x)/length(act_scored)
x <- 1:36
sapply(x,f)
qnorm(0.95,20.9,5.7)

p<-seq(0.01,0.99,0.01)
sample_quantiles <- quantile(act_scored, probs = p)
sample_quantiles

theoretical_quantiles <- qnorm(p,20.9,5.7)
qqplot(theoretical_quantiles,sample_quantiles)
