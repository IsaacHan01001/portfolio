library(tidyverse)
library(dslabs)
library(dplyr)
library(ggthemes)
library(ggrepel)
ds_theme_set()


data(murders)
p<-murders%>%ggplot(aes(population/10^6,total,label=abb))
p+geom_point(size=3)+
  geom_text(nudge_x=0.05)+
  scale_x_continuous(trans="log10")+
  scale_y_continuous(trans="log10")

#equivalently,

p<-murders%>%ggplot(aes(population/10^6,total,label=abb))+
  geom_text(nudge_x=0.075)+
  scale_x_log10()+
  scale_y_log10()+
  xlab("Population in millions (log scale)")+
  ylab("Total number of murders (log scale)")+
  ggtitle("US Gun Murders in US 2010")



r<-murders%>%
  summarize(rate=sum(total)/sum(population)*10^6)%>%
  pull(rate)


library(dslabs)
ds_theme_set()
library(ggthemes)
library(ggrepel)

p+geom_point(aes(col=region),size=3)+
  geom_abline(intercept=log10(r),lty=2,color="darkgrey")+
  scale_color_discrete(name="Region")+
  theme_economist()+
  theme_fivethirtyeight()  
    
