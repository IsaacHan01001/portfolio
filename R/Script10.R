library(dslabs)
data(murders)

pop<- murders$population
pop <- sort(pop)
pop

order(murders$population)[1]
murders$state[51]

which.min(murders$population)
murders$state[51]

temp<-c(35,88,42,84,81,30)
city<-c("Beijing", "Lagos","Paris","Rio de Jaeniro","San Juan","Toronto")
city_temps<-data.frame(name = city, temperature = temp)
ranks<-rank(murders$population)
my_df<-data.frame(murders$state,ranks)
my_df

ind<- order(murders$population)
my_df2<-data.frame(murders$state[ind],ranks[ind])
my_df2

data("na_example")
str(na_example)
mean(na_example)
ind<-!is.na(na_example)
mean(na_example[ind])

murder_rate <-murders$total/murders$population*100000
murders$abb[order(murder_rate)]

ind<-murder_rate<0.71
murders$state[ind]

sum(ind)
