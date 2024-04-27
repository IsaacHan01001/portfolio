library(tidyverse)
library(dslabs)
data(temp_carbon)
data("greenhouse_gases")
data("historic_co2")

temp_carbon%>%filter(!is.na(carbon_emissions))%>%.$year%>%max()
temp_carbon%>%filter(year%in%c(1751,2014))

temp_carbon%>%filter(!is.na(temp_anomaly))%>%.$year%>%min()
temp_carbon%>%filter(!is.na(temp_anomaly))%>%.$year%>%max()
temp_carbon%>%filter(year%in%c(1880,2018))

#4
p<-temp_carbon%>%filter(!is.na(year),!is.na(temp_anomaly))%>%ggplot(aes(year,temp_anomaly))
p+geom_line()+
  geom_hline(aes(yintercept=0,col=I("blue")))+
  ylab("Temperature anomaly (degree C)")+
  ggtitle("Temperature anomaly relative to 20th century mean, 1880-2018")+
  geom_text(aes(2000,0.05,label='20th century mean',col=I('blue')))+
  geom_line(aes(y=ocean_anomaly,color='red'))+
  geom_line(aes(y=land_anomaly,color='magenta'))

##p5

greenhouse_gases%>%
  ggplot(aes(year,concentration))+
  geom_line()+
  facet_grid(gas~.,scales = "free")+
  geom_vline(xintercept = 1850)
#####p10

temp_carbon%>%ggplot(aes(year,carbon_emissions))+
  geom_line()


###p11

co2_time<-historic_co2%>%ggplot(aes(year,co2))+
  geom_line()


##p12

co2_time+
  xlim(-8*10^5,-7.75*10^5)
  
co2_time+
  xlim(-3000,2018)

  
  