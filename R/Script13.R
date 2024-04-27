library(tidyverse)
library(dplyr)
library(dslabs)
data(murders)
murders<-mutate(murders,rate=total/population*10^5)
s<-murders%>%
  filter(region =="West")%>%
  summarize(minimum = min(rate),
            median = median(rate),
            maximum = max(rate))
s

#summarize

us_murder_rate <-murders%>%
  summarize(rate=sum(total)/sum(population)*10^5)
us_murder_rate

#quantile
x <-c(1,2,3,7,9)
quantile(x,c(0,0.5,1))

murders%>%
  filter(region =="West") %>%
  summarize(rarnge = quantile(rate,c(0,0.5,1)))

my_quantile <-function(x){
  r<- quantile(x,c(0,0.5,1))
  data.frame(minimum = r[1], median = r[2], maximum = r[3])
}
murders%>%
  filter(region =="West")%>%
  summarize(my_quantile(rate))

us_murder_rate<-murders%>%
  summarize(rate=sum(total)/sum(population)*10^5)%>%
  pull(rate)
us_murder_rate
class(us_murder_rate)

