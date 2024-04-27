library(dslabs)
data(heights)
options(digits = 3)    # report 3 significant digits for all answers

mean1<-mean(heights$height)

nrow(filter(heights,height>mean1,sex=="Female"))

data(heights)

sum(heights$sex=="Female")/length(heights$sex)
min(heights$height)
which.min(heights$height)
heights$height[1032]
min1<-min(heights$height)
which(min1==heights$height)
heights$height[1045]
max1<-max(heights$height)
min1<-min(heights$height)

sum(!(51:82 %in% heights$height))
heights2<-data.frame(sex = heights$sex, ht_cm=heights$height*2.54)
heights2%>%head()
heights2%>%filter(sex=="Female")%>%.$ht_cm%>%
  mean()

#####################
data(olive)
names(olive)
head(olive)
plot(olive$palmitic,olive$palmitoleic)

hist(olive$eicosenoic)
olive%>%group_by(region)

boxplot(palmitic~region,olive)

