x<-c(FALSE,TRUE,FALSE,TRUE,TRUE,FALSE)
which(!x)

index <- which(x == TRUE)
index

index<-match(c("New York","Florida","Texas"),murders$state)
murders$state[index]
murder_rate = murders$total/murders$population*100000
murder_rate[index]

x<-c("a","b","c","d","e")
y <-c("a","d","f")

y %in% x

c("Boston","Dakota","Washington")%in%murders$state

which(murders$state=="Massachusetts")
match(c("Massachusetts"),murders$state)


match("a",murders$state)

 