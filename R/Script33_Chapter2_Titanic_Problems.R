library(titanic)
library(tidyverse)
library(dplyr)
library(dslabs)
library(patchwork)
options(digits=3)
data("titanic_train")

titanic<-titanic_train%>%
  select(Survived,Pclass,Sex,Age,SibSp,Parch,Fare)%>%
  mutate(Survived=factor(Survived),
         Pclass=factor(Pclass),
         Sex=factor(Sex))

p<-titanic%>%filter(!is.na(Age))
p%>%ggplot(aes(x=Age,y=after_stat(count),color=Sex))+
  geom_density()

p%>%ggplot(aes(sample=Age))+
  geom_qq()+
  facet_grid(.~Sex)

males<-titanic%>%filter(Sex=="male")
females<-titanic%>%filter(Sex=="female")
na_num1<-sum(is.na(males$Age))
num1<-sum(between(males$Age,0,16),na.rm=TRUE)/(nrow(males)-na_num)

na_num2<-sum(is.na(females$Age))
num2<-sum(between(females$Age,0,16),na.rm=TRUE)/(nrow(males)-na_num)

num1
num2

ind1<-which.max(titanic$Age)
titanic[ind1,]
######################## problem#2

params<-titanic%>%
  filter(!is.na(Age))%>%
  summarize(mean=mean(Age),sd=sd(Age))

p%>%ggplot(aes(sample=Age))+
  geom_qq(dparams=params)+
  geom_abline()

#######  problem#3


dat<-titanic%>%group_by(Sex)%>%count(Survived)%>%mutate(proportions1=n/sum(n)) 

p1<-dat%>%filter(Survived==1)%>%ggplot(aes(Sex,proportions1,fill=Sex))+
  geom_bar(stat = "identity",position=position_dodge(),alpha=0.2)+
  geom_bar(stat="identity",aes(Sex,y=1),alpha=0.3)
p1

######## problem#4


p1<-titanic%>%filter(Survived==1)

titanic%>%
  ggplot(aes(x=Age,y=after_stat(count),fill=I('blue')))+
  geom_density(alpha=0.2)+
  geom_density(aes(y=1/2*after_stat(count),color=I('black'),fill=NULL))+
  geom_density(data=p1,aes(x=Age,y=after_stat(count)),alpha=0.3,fill='red')


# Problem #6

titanic%>%filter(Fare!=0)%>%ggplot(aes(Survived,Fare))+
  geom_boxplot()+
  scale_y_continuous(trans="log2")+
  geom_jitter(alpha=0.5)

# Problem#7

titanic%>%ggplot(aes(Pclass,fill=Survived))+
  geom_bar()+
titanic%>%ggplot(aes(Pclass,fill=Survived))+
  geom_bar(position=position_fill())+
titanic%>%ggplot(aes(Survived,fill=Pclass))+
  geom_bar()

##Problem#8

titanic%>%ggplot(aes(Age,after_stat(count),fill=Survived))+
  geom_density()+
  facet_grid(Sex~Pclass)
9