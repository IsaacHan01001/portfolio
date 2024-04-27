library(dslabs)
library(dplyr)
library(tidyverse)
data(gapminder)

gapminder<-gapminder%>%
  mutate(dollars_per_day=gdp/population/365)
west<-c("Western Europe", "Northern Europe",
        "Southern Europe", "Northern America", "Australia and New Zealand")

#facet by West vs developing
gapminder%>%
  filter(year==1970&!is.na(gdp))%>%
  mutate(group=ifelse(region%in%west,"West","Developing"))%>%
  ggplot(aes(dollars_per_day))+
  geom_histogram(binwidth=1,color="black")+
  scale_x_continuous(trans="log2")+
  facet_grid(.~group)

#facet to compare 1970 & 2010
gapminder%>% 
  filter(year %in% c(1970,2010) & !is.na(gdp))%>%
  mutate(group = ifelse(region%in%west,"West", "Developing"))%>%
  ggplot(aes(dollars_per_day))+
  geom_histogram(binwidth=1,color="black")+
  scale_x_continuous(trans="log2")+
  facet_grid(year ~group)

#set intersection
country_list_1 <-gapminder%>%
  filter(year==1970 &!is.na(dollars_per_day))%>%.$country
country_list_2<-gapminder%>%
  filter(year==2010&!is.na(dollars_per_day))%>%.$country
country_list<-intersect(country_list_1,country_list_2)
###
gapminder%>% 
  filter(year %in% c(1970,2010) & !is.na(gdp) &country%in%country_list)%>%
  mutate(group = ifelse(region%in%west,"West", "Developing"))%>%
  ggplot(aes(dollars_per_day))+
  geom_histogram(binwidth=1,color="black")+
  scale_x_continuous(trans="log2")+
  facet_grid(year ~group)


###
p<-gapminder%>% 
  filter(year %in% c(1970,2010) & !is.na(gdp) &country%in%country_list)%>%
  mutate(region=reorder(region,dollars_per_day,FUN=median))%>%
  ggplot()+
  theme(axis.text.x = element_text(angle=45,hjust=1))+
  xlab("")+
  scale_y_continuous(trans="log2")

p+geom_boxplot(aes(region,dollars_per_day,fill=factor(year)))
#facet_grid(year~.)
#########################

country_list_1 <-gapminder%>%
  filter(year==1970 &!is.na(dollars_per_day))%>%.$country
country_list_2<-gapminder%>%
  filter(year==2010&!is.na(dollars_per_day))%>%.$country
country_list<-intersect(country_list_1,country_list_2)
west<-c("Western Europe", "Northern Europe",
        "Southern Europe", "Northern America", "Australia and New Zealand")
gapminder%>%
  filter(year==1970&country %in%country_list)%>%
  mutate(group = ifelse(region%in%west,"West","Developing"))%>%
  group_by(group)%>%
  summarize(n=n())%>%knitr::kable()


p<-gapminder%>%
  filter(year%in% c(1970,2010)&country %in% country_list)%>%
  mutate(group = ifelse(region %in% west, "West"," Developing"))%>%
  ggplot(aes(dollars_per_day, y=..count..,fill=group))+
  scale_x_continuous(trans="log2")
p+geom_density(alpha=0.2,bw=0.75)+facet_grid(year ~.)

##### 
gapminder_1<-gapminder%>%
  mutate(group=case_when(
    .$region%in%west~"West",
    .$region %in% c("Eastern Asia","South-Eastern Asia")~"East Asia",
    .$region%in% c("Caribbean","Central America","South America")~"Latin America",
    .$continent == "Africa" &.$region != "Northern Africa" ~"Sub-Saharan Africa",
    TRUE~"Others"))
gapminder_2<-gapminder_1%>%filter(!is.na(gdp))%>%
  mutate(group=factor(group,levels=c('Others','Latin America','East Asia','Sub-Saharan Africa','West')))

####
p<-gapminder_2%>%
  filter(year%in%c(1970,2012)&country%in% country_list)%>%
  ggplot(aes(dollars_per_day,fill=group))+
  scale_x_continuous(trans="log2")

###
p+geom_density(alpha=0.2,bw=0.75,position='stack')+
  facet_grid(year~.)


###weighted Stack
gapminder_2 %>%
  filter(year %in% c(1970,2010) & country %in% country_list) %>%
  group_by(year)%>%
  mutate(weight=population/sum(population))%>%
  ungroup()%>%
  ggplot(aes(dollars_per_day,fill=group,weight=weight))+
  scale_x_continuous(trans="log2")+
  geom_density(alpha=0.2,bw=0.75,position = "stack")+
  facet_grid(year~.)
test1
