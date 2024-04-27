library(gtools)
library(tidyverse)

ways <- permutations(8,3)
nrow(ways)
1/8*1/7*1/6

set.seed(1, sample.kind = "Rounding")
runners <- rep(c("Jameica","USA","Ecuador",
                 "Netherlands","France","South Africa"),
               times = c(3,1,1,1,1,1))

result2<-replicate(10^4,{
  medalist <-sample(runners,3)
  all(medalist%in%"Jameica")
})
mean(result2)


# Question2 ---------------------------------------------------------------
nrow(combinations(6,2))

6*15*3
n<-1:12
sapply(n,nrow(combinations(n,2))*45)

# Question 2e -------------------------------------------------------------

side_choices <- function(x){
  18*nrow(combinations(x,2))
}
combos<- sapply(2:12,entree_choices)

data.frame(sides =2:12, combos = combos)%>%
  filter(combos>365)%>%
  min(.$sides)


# Question3 ---------------------------------------------------------------

library(tidyverse)
head(esoph)
str(esoph)

all_cases<-sum(esoph$ncases)
all_controls<-sum(esoph$ncontrols)

q1<-esoph%>%filter(alcgp == max(alcgp))
a<-sum(q1$ncases)
b<-sum(q1$ncontrols)
a/(a+b)

q2<-esoph%>%filter(alcgp == min(alcgp))
a2<-sum(q2$ncases)
b2<-sum(q2$ncontrols)
a2/(a2+b2)

q3 <- esoph%>%filter(ncases !=0)%>%
  summarize(ncases = sum(ncases))
q3
q4 <-esoph%>%filter(ncases !=0 & tobgp!= "0-9g/day" )%>%
  summarize(ncases = sum(ncases))
q4
q3
122/200

q5<-esoph%>%filter(tobgp!="0-9g/day")
sum(q5$ncontrols)/sum(esoph$ncontrols)

# Question #5 -------------------------------------------------------------

q1 <- esoph%>%filter(alcgp == max(alcgp))%>%.$ncases%>%sum()
q1

esoph%>%summarize(rate= q1/sum(ncases))

# 5b ----------------------------------------------------------------------

q1 <- esoph%>%filter(tobgp==max(tobgp))%>%.$ncases%>%sum()
q2 <- esoph%>% .$ncases%>%sum()
q1/q2

# 5c ----------------------------------------------------------------------

q1 <- esoph%>% filter(alcgp==max(alcgp),tobgp==max(tobgp))%>%.$ncases%>%sum()
q1/q2

# 5d ----------------------------------------------------------------------

q1 <- esoph %>% filter(alcgp==max(alcgp) | tobgp==max(tobgp))%>%.$ncases %>% 
  sum()
q1
q1/q2

# 6a ----------------------------------------------------------------------

q1 <- esoph %>% filter(alcgp==max(alcgp)) %>% .$ncontrols %>% sum()
q1
q2 <- esoph %>% .$ncontrols %>% sum() 
q1/q2

# 6b ----------------------------------------------------------------------

q2 <- esoph %>% .$ncases %>% sum()
q1<-esoph%>%filter(alcgp==max(alcgp))%>%.$ncases %>% sum() 
r1 <- q1/q2

q4 <- esoph %>% .$ncontrols %>% sum()
q3 <- esoph %>% filter(alcgp==max(alcgp)) %>% .$ncontrols %>% sum()
r2 <- q3/q4
r1
r2
r1/r2

# 6c ----------------------------------------------------------------------

q1 <- esoph %>% .$ncontrols %>% sum()
q2 <- esoph %>% filter(tobgp==max(tobgp)) %>% .$ncontrols %>% sum()
q2/q1

# 6d ----------------------------------------------------------------------

q1 <- esoph %>% .$ncontrols %>% sum()
q2 <- esoph %>% filter(tobgp==max(tobgp),alcgp==max(alcgp)) %>% .$ncontrols %>% sum()
q2/q1


# 6e ----------------------------------------------------------------------

q1 <- esoph %>% .$ncontrols %>% sum()
q2 <- esoph %>% filter(tobgp==max(tobgp) | alcgp==max(alcgp)) %>% .$ncontrols %>% sum()
q2/q1

# 6f ----------------------------------------------------------------------
q3 <- esoph %>% .$ncases %>% sum()
q4 <- esoph %>% filter(tobgp==max(tobgp) | alcgp==max(alcgp)) %>% .$ncases %>% sum()
r1<-q4/q3

q1 <- esoph %>% .$ncontrols %>% sum()
q2 <- esoph %>% filter(tobgp==max(tobgp) | alcgp==max(alcgp)) %>% .$ncontrols %>% sum()
r2<-q2/q1

r1/r2
