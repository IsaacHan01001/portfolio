library(dslabs)
murder_rate<-murders$total/murders$population*100000
index<-murder_rate <=0.71
index
murders$state[index]


west<-murders$region ==levels(murders$region)[4]
safe <- murder_rate<=1 
safe
west
index <- west&safe
index
murders$state[index]
