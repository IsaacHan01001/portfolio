set.seed(1, sample.kind = "Rounding")
number<- "Three"
suit <- "Hearts"
paste(number,suit)
paste(letters[1:5], 1:5)

expand.grid(pants = c("blue","black"), shirt = c("white","grey","plaid"))

suits <- c("Diamonds","Clubs","Hearts","Spades")
numbers <- c("Ace", "Deuce", "Three", "Four","Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack",
             "Queen","King")
deck <- expand.grid(number= numbers, suit = suits)
deck2 <- paste(deck$number, deck$suit)
deck2

kings<-paste("King", suits)
kings

mean(deck2%in%kings)


library(gtools)
permutations(7,2)

all_phone_numbers <- permutations(10,7, v= 0:9)
n<- nrow(all_phone_numbers)
index<-sample(n,5)
all_phone_numbers[index,]


# Permutation Card --------------------------------------------------------


hands<- permutations(52,2, v=deck2)
hands
first_card<-hands[,1]
second_card<-hands[,2]
first_card
second_card


# Sum card ----------------------------------------------------------------

sum(first_card %in% kings & second_card %in% kings)/
  sum(first_card %in% kings)

# Combinations ------------------------------------------------------------

combinations(3,2)
aces <- paste("Ace", suits)
facecard <- c("King","Queen","Jack","Ten")
facecard <- expand.grid(number=facecard,suit=suits)
facecard
facecard <- paste(facecard$number,facecard$suit)
facecard

hands <- combinations(52,2,v=deck2)
hands

mean(hands[,1] %in% aces & hands[,2] %in% facecard)


# Simulation --------------------------------------------------------------

hand <- sample(deck2,2)
hand

B <- 10000
results <- replicate(B, {
  hand <- sample(deck2,2)
  (hand[1] %in% aces & hand[2] %in% facecard)|
    (hand[2] %in% aces & hand[1] %in% facecard)
    
})
mean(results)
