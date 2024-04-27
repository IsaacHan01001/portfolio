library(tidyverse)
library(dslabs)
data(heights)
x <- heights %>% filter(sex=="Male") %>% .$height

F <- function(a) mean(x<=a)
1-F(70)


# Cdf Norm ----------------------------------------------------------------

1-pnorm(70.5,mean(x),sd(x))
sd

plot(prop.table(table(x)), xlab=" a = Height in inches", ylab= "Pr(x-a)")
a1 <- mean(x <= 68.5) - mean(x<=67.5)
a2 <- mean(x <= 69.5) - mean(x<=68.5)
a3 <- mean(x <= 70.5) - mean(x<=69.5)

b1 <- pnorm(68.5, mean(x),sd(x))-pnorm(67.5,mean(x),sd(x))
b2 <- pnorm(69.5, mean(x),sd(x))-pnorm(68.5,mean(x),sd(x))
b3 <- pnorm(70.5, mean(x),sd(x))-pnorm(69.5,mean(x),sd(x))

a1-b1
a2-b2
a3-b3


# dnorm -------------------------------------------------------------------

x <- seq(-4,4,length = 100)
data.frame(x,f=dnorm(x)) %>% 
  ggplot(aes(x,f))+
  geom_line()

plot(x,dnorm(x,mean(x),sd(x)))

# Rnorm -------------------------------------------------------------------

x <- heights %>% filter(sex=="Male") %>% .$height
n <- length(x)
avg <- mean(x)
s <- sd(x)
simulated_heights <- rnorm(n,avg,s)
ds_theme_set()

data.frame(simulated_heights=simulated_heights) %>% ggplot(aes(simulated_heights))+
  geom_histogram(col ='black', binwidth  =2)



# Monte Carlo Simulation of heights ---------------------------------------

B <- 10000
tallest <- replicate(B,{
  simulated_data <- rnorm(800,avg,s)
  max(simulated_data)
})

mean(tallest>=84)

# other distributions -----------------------------------------------------


