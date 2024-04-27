a<-murders%>%group_by(region)%>%summarize(median=median(rate))
a

murders%>%arrange(region,rate)%>%top_n(-150)

#DATACAMP
library(NHANES)
data(NHANES)
library(dslabs)
data("na_example")
mean(na_example)
sd(na_example)
mean(na_example,na.rm=TRUE)
sd(na_example,na.rm=TRUE)

