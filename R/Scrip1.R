library(tidyverse)
library(dslabs)
data(murders)
class(murders)
str(murders)
head(murders)
names(murders)
murders$population
murders
pop <- murders$population
length(pop)
a <- 1
"a"
z <- 3==2
class(z)
A <- murders$region
class(A)
levels(A)

region<- murders$region
value <- murders$total
region <- reorder(region, value, FUN = sum)
levels(region)
