library(dslabs)
data(murders)
str(murders)
names(murders)
a<-murders$state
class(a)
b<-murders[["state"]]
identical(a,b)
class(murders$region)
length(levels(murders$region))
murders$region
table(murders$region)

temp = c(35, 88, 42, 84, 81,30)
  
result = c("Beijing"=35, "Lagos" = 88, "Paris" = 42, "Rio de Janeiro" = 84,
         "San Juan" = 81, "Toronto" = 30)

city<- c("Beijing","Lagos","Paris","Rio de Janeiro","San Juan","Toronto")
names(temp) <-city
temp

temp[1:3]
temp[c("Paris","San Juan")]
12:73
seq(1,100,2)
length(seq(6,55,4/7))
class(seq(1,10,0.5))
class(seq(1,10))

max(murder_rate)
min(murder_rate)

ind<-which.max(murder_rate)
murders$state[ind]
ind2<-which.min(murder_rate)
murders$state[ind2]

data(murders)
x<-c(31,4,15,92,65)
sort(x)
x[order(x)]

ind<-order(murders$total)
murders$abb[ind]
