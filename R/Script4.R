library(dslabs)
data(murders)
sort(murders$total)

x <- c(31,4,15,92,65)
sort(x)
index <-order(x)
index

index <- order(murders$total)
index
murders$abb[index]

max(murders$total)
i_max<- which.max(murders$total)
i_max
murders$state[i_max]

min(murders$total)
i_min<-which.min((murders$total))
i_min
murders$state[i_min]

x<-c(31,4,15,92,65)
rank(x)
