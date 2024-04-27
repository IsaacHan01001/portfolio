x <- c(1,"canada",3)
x
class(x)
x <- 1:5
y <- as.character(x)
z <- as.numeric(y)
z

x <- c("1","b","3")
as.numeric(x)

x = c(1,5,6)
class(x)
x <- 3,"b",8
x <- c(4,"seven",9)
class(x)
x = "z"
class(x)

record <- list(name = "John Doe", student_id = 1234, 
               grades = c(95,82,91,97,93),grades = "A")
names(record)
record$student_id
record[["student_id"]]

mat <- matrix(1:12,4,3)
mat[1:2,]
as.data.frame(mat)

library(dslabs)
data("murders")
murders[25,1]
murders[2:3,]


