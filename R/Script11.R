library(dslabs)
c("Boston","Dakota","Washington")%in%murders$state
match(c("New York","Florida", "Texas"),murders$state)

which(murders$state%in%c("New York","Florida", "Texas"))

library(dplyr)
murders <- mutate(murders,rate=total/population*100000)
murders
head(murders)
filter(murders,rate<=0.71)
new_table <-select(murders,state,region,rate)
new_table


murders%>%mutate(murders,rate=total/population*100000)%>%select(state,region,rate)%>%filter(rate<=0.71)

grades<- data.frame(names=c("John","Juan","Jean","Yao"),
                    exam_1 = c(95,80,90,85), exam_2 = c(90,85,85,90))
grades
class(grades$names)

