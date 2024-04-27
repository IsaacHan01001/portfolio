library(dslabs)
library(dplyr)
data(heights)
filtered<-filter(heights,sex=="Male")
x<-c(mean(filtered$height),sd(filtered$height))
a<-70.5
1-pnorm(a,x[1],x[2])

#
x<-heights%>%filter(sex=="Male")%>%pull(height)
x
plot(prop.table(table(x)),xlab ="a= Height in inches", ylab = "Pr(x=a)")

x1<-c(mean(x<=68.5)-mean(x<=67.5), mean(x<=69.5)-mean(x<=68.5), mean(x<=70.5)-mean(x<=69.5))
x2<-c(pnorm(68.5,mean(x),sd(x))-pnorm(67.5,mean(x),sd(x)), 
      pnorm(69.5,mean(x),sd(x))-pnorm(68.5,mean(x),sd(x)),
      pnorm(70.5,mean(x),sd(x))-pnorm(69.5,mean(x),sd(x)))
abs(x1-x2)


summary(heights$height)
p<-seq(0.01,0.99,0.01)
p
percentiles<-quantile(heights$height,p)
percentiles
percentiles[names(percentiles)=="25%"]

p <- seq(0.01, 0.99, 0.01)
theoretical_quantiles <- qnorm(p, 69, 3)
theoretical_quantiles

x<-heights$height[heights$sex=="Male"]
z<-scale(x)
mean(x<=69.5)
p<-seq(0.05,0.95,0.05)
observed_quantiles<-quantile(x,p)
observed_quantiles
qnorm()
theoretical_quantiles<-qnorm(p,mean=mean(x),sd=sd(x))
theoretical_quantiles[10]
plot(theoretical_quantiles,observed_quantiles)
abline(0,1)

observed_quantiles2<-quantile(z,p)
theoretical_quantiles<-qnorm(p)
plot(theoretical_quantiles,observed_quantiles2)
abline(0,1)
