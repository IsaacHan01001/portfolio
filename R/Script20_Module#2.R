library(dslabs)
library(dplyr)
data(heights)

#tabulated as ratio
prop.table(table(heights$sex))
heights$sex%>%table()%>%prop.table()

#how to create cdf(Cumulative Distribution Function)
my_data =heights$height
a<-seq(min(my_data),max(my_data), length=100)
cdf_function<-function(x){
  mean(my_data<=x)
}
cdf_values<-sapply(a,cdf_function)
plot(a,cdf_values)
hist(heights$height)

#normal distribution
library(tidyverse)
library(dslabs)
data(heights)
index<-heights$sex=="Male"
x<-heights$height[index]
c(average=mean(x),SD=sd(x))
z<-scale(x)
abs(z)<2

