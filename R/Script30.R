library(dslabs)
library(dplyr)
library(tidyverse)
data(gapminder)

gapminder<-gapminder%>%
  mutate(dollars_per_day=gdp/population/365)
west<-c("Western Europe", "Northern Europe",
        "Southern Europe", "Northern America", "Australia and New Zealand")

gapminder_1<-gapminder%>%
  mutate(group=case_when(
    .$region%in%west~"The West",
    .$region %in% "Northern Africa"~"Northern Africa",
    .$region %in% c("Eastern Asia","South-Eastern Asia")~"East Asia",
    .$region =="Southern Asia"~"Southern Asia",
    .$region%in% c("Caribbean","Central America","South America")~"Latin America",
    .$continent == "Africa" &.$region != "Northern Africa" ~"Sub-Saharan Africa",
    .$region %in% c("Melanesia","Micronesia","Polynesia")~"Pacific Islands",
    TRUE~"Others"))
surv_income<- gapminder_1%>%
  filter(year==2010, !is.na(gdp),!is.na(infant_mortality),!is.na(group))%>%
  group_by(group)%>%
  summarize(income=sum(gdp)/sum(population)/365,
            infant_survival_rate=1-sum(infant_mortality/1000*population)/sum(population))
surv_income%>%arrange(desc(income))

gapminder_2<-gapminder_1%>%filter(!is.na(gdp))%>%
  mutate(group=factor(group,levels=c('Others','Latin America','East Asia','Sub-Saharan Africa','West')))
