
# MontyHall ---------------------------------------------------------------

B <- 10^4
stick<- replicate(B,{
  doors <- as.character(1:3)
  prize<- sample(c("car","goat","goat"))
  prize
  prize_door <- doors[prize == "car"]
  my_pick <- sample(doors,1)
  show <- sample(doors[!doors%in% c(my_pick,prize_door)],1)
  stick <- my_pick
  stick == prize_door
})
mean(stick)


# Switch ------------------------------------------------------------------

B <- 10^4
stick<- replicate(B,{
  doors <- as.character(1:3)
  prize<- sample(c("car","goat","goat"))
  prize_door <- doors[prize == "car"]
  my_pick <- sample(doors,1)
  show <- sample(doors[!doors%in% c(my_pick,prize_door)],1)
  stick <- my_pick
  switch <- doors[!doors%in% c(my_pick, show)]
  switch == prize_door
})
mean(stick)

# Datacamp1 ---------------------------------------------------------------

n <- 6
outcome <- sample(c(0,1))

l <- rep(list(outcome),n)  
l

possibilities <- expand.grid(l)
possibilities

results <-rowSums(possibilities)>=4
results

sum(results)/length(results)

mean(results)

# DataCamp2 ---------------------------------------------------------------

B <- 10^4
set.seed(1)
results <- replicate(B,sample(c(0,1),replace = TRUE,6))
results
mean(colSums(results)>=4)

# DataCamp4 ---------------------------------------------------------------

N<-1:4
N
