n <- 50
bdays <- sample(1:365, n, replace=TRUE)
sum(duplicated(bdays))

# MonteCarlo-Birthdays ----------------------------------------------------


B <- 10000
results <- replicate(B,{
  bdays<-sample(1:365,n,replace=TRUE)
  any(duplicated(bdays))
})
mean(results)


# Bdays with different n --------------------------------------------------


compute_prob <- function(n, B=10000){
  same_day <- replicate(B,{
    bdays <- sample(1:365,n,replace=TRUE)
    any(duplicated(bdays))
  })
  mean(same_day)
}
n <- seq(1,60)


# For loop ----------------------------------------------------------------

prob <- sapply(n,compute_prob)
plot(n,prob)


# Exact Probability -------------------------------------------------------

exact_prob <- function(n){
  prob_unique <- seq(365, 365-n+1)/365
  1-prod(prob_unique)
}

eprob <- sapply(n,exact_prob)
plot(n,prob)
lines(n,eprob,col="red")


# Stability Analysis ------------------------------------------------------

B <- 10^seq(1,5,len=100)
compute_prob <- function(B,n=22){
  same_day <- replicate(B,{
    bdays <- sample(1:365, n, replace = TRUE)
    any(duplicated(bdays))
  })
  mean(same_day)
}

prob <- sapply(B,compute_prob)
plot(log10(B),prob,type = "l")
    
