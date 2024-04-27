library(tidyverse)
library(dslabs)
library(data.table)
data(murders)
select(murders,state,region)

murders<-setDT(murders)
murders[,c("state","region")] |> head()
murders[,.(state,region)]|>head()

data(murders)
murders1<-mutate(murders,rate=total/population*10^5)

murders2<-setDT(murders)
murders2[,rate :=total/population*10^5]|>head()
murders[,":="(rate=total/population*10^5,rank = rank(population))]|>head()

x<-data.table(a=1)
y<-x
x[,a:=2]
y

y[,a:=1]
x

x<-data.table(a=1)
y<-copy(x)
x[,a:=2]
y


murders[rate<=0.7, .(state,rate)]
