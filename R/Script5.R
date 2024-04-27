library(dslabs)
murders$state[which.max(murders$population)]
max(murders$population)

heights<-c(69,62,66,70,70,73,67,73,67,70)
heights*2.54
heights -69

murder_rate <-murders$total/murders$population*100000
murders$state[order(murder_rate,decreasing=TRUE)]

x<-c(2,43,27,96,18)
sort(x)
rank(x)
order(x)

name <- c("Mandi","Amy","Nicole","Olivia")
distance <-c(0.8,3.1,2.8,4.0)
time<-c(10,30,40,50)
time<-time/60
time
speed<-distance/time
speed

