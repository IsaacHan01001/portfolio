set.seed(1, sample.kind = "Rounding")

beads<- rep(c("red","blue"),times=c(2,3))
beads
sample(beads,1)
B<-10000
events<-replicate(B,sample(beads,1))
tab<- table(events)
tab
prop.table(tab)

sample(beads,replace=TRUE,6)
mean(beads=="blue")

set.seed(1, sample.kind = "Rounding")
x<-sample(beads,5)
x[2:5]

set.seed(1, sample.kind = "Rounding")
beads <-rep(c("cyan","magenta","yellow"),time= c(3,5,7))
beads
