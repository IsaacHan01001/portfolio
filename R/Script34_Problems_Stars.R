library(tidyverse)
library(dplyr)
library(dslabs)
library(patchwork)
library(ggrepel)
library(RColorBrewer)
options(digits=3)
data(stars)

#1
P1<-stars%>%summarize(avg=mean(magnitude),sd=sd(magnitude))

#2
stars%>%ggplot(aes(magnitude))+
  geom_density()

#3
stars%>%ggplot(aes(temp))+
  geom_density()
#4
stars%>%ggplot(aes(x=log10(temp),y=magnitude,label=star,color=type))+
  geom_point()+
  scale_y_reverse()+
  scale_x_reverse()+
  scale_color_manual(values=brewer.pal(10,"Paired"))
  
#  geom_text_repel()
RColorBrewer::brewer.pal.info

#%


