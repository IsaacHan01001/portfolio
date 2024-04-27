library(dslabs)
library(tidyverse)
library(dplyr)
data(gapminder)
head(gapminder)

compare<-function(name1,name2){
  gapminder%>%
    filter(year==2015,country %in% c(name1,name2))%>%
    select(country,infant_mortality)
  
}
compare("Sri Lanka", "Turkey")
compare("Poland", "South Korea")
compare("Malaysia", "Russia")
compare("Pakistan", "Vietnam")
compare("Thailand", "South Africa")

ds_theme_set()
filter(gapminder,year==1962 )%>%
  ggplot(aes(fertility,life_expectancy,color=continent))+
  geom_point()

gapminder%>%filter(country%in%c("South Korea","Germany"))%>%
  ggplot(aes(year,fertility,group=country,col=country))+
  geom_line()

#add label
labels<-data.frame(country=c("South Korea","Germany"), x=c(1975,1965),y=c(60,72))
gapminder%>%filter(country %in% c("South Korea","Germany")) %>%
  ggplot(aes(year,life_expectancy, col= country))+
  geom_line()+
  geom_text(data=labels, aes(x,y,label= country),size=5)+
  theme(legend.position="none")
