library(dslabs)
library(data.table)
library(dplyr)
data(gapminder)
gapminder%>%head()
as_tibble(gapminder)%>%head()
class(as_tibble(murders[,1]))

tibble(id=c(1,2,3),func=c(mean,median,sd))
