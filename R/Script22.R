library(tidyverse)
library(dslabs)


p<-murders%>%ggplot()+
  geom_point(aes(x=population/10^6,y=total),size=3)+
  geom_text(aes(population/10^6,total,label=abb),nudge_x=1)

p



q<-murders%>% ggplot(aes(population/10^6,total,label=abb))
q+geom_point(size=3)+geom_text(aes(x=10,y=800,label="Hello there!"),nudge_x=1.5)

