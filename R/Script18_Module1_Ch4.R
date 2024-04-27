library(dslabs)
data(murders)
murder_rate<-murders$total/murders$population*10^5

ind<-which.min(murder_rate)
if(murder_rate[ind]<0.25){
  print(murders$state[ind])
}else{
  print("No state has a murder rate that low")
}

ifelse(a>0,1/a,NA)


if(a!=0){
  print(1/a)
} else{
  print("No reciprocal for 0.")
}


a<-c(0,1,2,-4,5)
result<-ifelse(a>0,1/a,NA)
result
data("na_example")
sum(is.na(na_example))
no_nas<-ifelse(is.na(na_example),0,na_example)
sum(is.na(no_nas))

z<-c(TRUE,TRUE,FALSE)
any(z)
all(z)

avg<-function(x){
  s<-sum(x)
  n<-length(x)
  s/n
}
avg(c(1,2,3))
identical(mean,avg)

avg <- function(x,arithmetic=TRUE){
  n<-length(x)
  ifelse(arithmetic,sum(x)/n,prod(x)^(1/n))
}
avg(1:100,arithmetic=FALSE)

x<-25
s<-5
test<-function(x){
  s<-1/x
}

test(2)







