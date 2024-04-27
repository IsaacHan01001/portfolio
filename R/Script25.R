library(dslabs)
library(dplyr)
library(tidyverse)
data(heights)

x<-heights%>%filter(sex=="Male")

p<-heights%>%
  filter(sex=="Male")%>%
  ggplot(aes(x=height))

#histogram
p+geom_histogram(binwidth = 1,fill="blue",col="black")+
  xlab("Male heights in inches")+
  ggtitle("Histogram")
  

#geom_density
p+geom_density(fill="blue")
  
#geom_qqp lot

p<-heights%>%filter(sex=="Male")%>%
  ggplot(aes(sample=height))
p+geom_qq()

#using dprams with qq
params<-heights%>%
  filter(sex=="Male")%>%
  summarize(mean=mean(height),sd=sd(height)) 
q1<-p+geom_qq(dparams=params)+
  geom_abline()

#cleaner coding-with z score
q2<-heights%>%filter(sex=="Male")%>%
  ggplot(aes(sample=scale(height)))+
  geom_qq()+
  geom_abline()
#cleaner coding-with z score
q3<-heights%>%filter(sex=="Male")%>%
  ggplot(aes(sample=scale(height)))+
  geom_qq()+
  geom_abline()
library(gridExtra)
grid.arrange(q1,q2,q3,ncol=3)


p<-heights%>%filter(sex=="Male")%>%ggplot(aes(x=height))
p1<-p+geom_histogram(binwidth = 1, fill ="blue", col="black")
p2<-p+geom_histogram(binwidth = 2, fill ="blue", col="black")
p3<-p+geom_histogram(binwidth = 3, fill ="blue", col="black")
grid.arrange(p1,p2,p3,ncol=3)

heights%>%ggplot(aes(height,group=sex,color=sex,fill=sex))+
  geom_density(alpha=0.9)

#faceting
filter(gapminder,year%in%c(1962,2012))%>%
  ggplot(aes(fertility,life_expectancy, col=continent))+
  geom_point()+
  facet_grid(continent~year)
#faceting2
filter(gapminder,year%in%c(1962,2012))%>%
  ggplot(aes(fertility,life_expectancy, col=continent))+
  geom_point()+
  facet_grid(.~year)
#faceting3
years<-c(1962,1980,1990,2000,2012)
continents<-c("Europe","Asia")
gapminder%>%
  filter(year%in%years &continent %in% continents)%>%
  ggplot(aes(fertility,life_expectancy, col=continent))+
  geom_point()+
  facet_wrap(~year)
