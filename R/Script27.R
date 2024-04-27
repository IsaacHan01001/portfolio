library(dplyr)
library(dslabs)
library(tidyverse)
gapminder<-gapminder%>%
  mutate(dollars_per_day=gdp/population/365)

#original plot
p1<-gapminder%>% filter(year== 1970 &!is.na(gdp))%>%
  ggplot(aes(dollars_per_day))+
  geom_histogram(binwidth=1,color='black')



#log2 transformation
p2<-gapminder%>% filter(year== 1970 &!is.na(gdp))%>%
  ggplot(aes(log2(dollars_per_day)))+
  geom_histogram(binwidth=1,color='black')

#log2 transformation
p3<-gapminder%>% filter(year== 1970 &!is.na(gdp))%>%ggplot(aes(dollars_per_day))+
  geom_histogram(binwidth=1,color='black')+
  scale_x_continuous(trans = "log2")

library(gridExtra)
grid.arrange(p1,p2,p3,ncol=3)  

#box_plots

length(levels(gapminder$region))
p<-gapminder%>%
  filter(year==1970,!is.na(gdp))%>%
  ggplot(aes(region,dollars_per_day))
p+geom_boxplot()+
  theme(axis.text.x=element_text(angle=45,hjust=1))


fac1<-factor(c("Asia","Asia","West","West","West"))
levels(fac1)
value<-c(10,11,12,6,4)
fac2<-reorder(fac1,value,FUN=mean)
fac2

#
p<- gapminder %>%
  filter(year == 1970 & !is.na(gdp))%>%
  mutate(region=reorder(region,dollars_per_day,FUN=median))%>%
  ggplot(aes(region,dollars_per_day,fill=continent ))+
  geom_boxplot()+
  theme(axis.text.x=element_text(angle=45,hjust=1))+
  scale_y_continuous(trans="log2")+
  geom_point(show.legend = FALSE)
