library(tidyverse)
library(gutenbergr)
library(tidytext)
library(dplyr)
options(digits = 3)
head(gutenberg_metadata)
data("stop_words")

gutenberg_metadata %>% filter(str_detect(title, "Pride and Prejudice"))
gutenberg_works(languages = "en") %>% filter(str_detect(title, "Pride and Prejudice"))
gutenberg_works(title == "Pride and Prejudice")$gutenberg_id
text <- gutenberg_download(1342, mirror ="http://mirror.csclub.uwaterloo.ca/gutenberg/")
text_df <- tibble(text)
result <- text_df %>% unnest_tokens(word, text)
filteredstops <- result %>% anti_join(stop_words)
filteredstops %>% nrow()

test1 <- filteredstops %>% filter(!str_detect(word, "[0-9]"))
test2 <- filteredstops %>% filter(str_detect(word, "[^0-9]"))

anti_join(test2, test1)

str_detect("_15th", "[0-9]")
str_detect("_15th", "[^0-9]")
str_detect("15t", "[^0-9]")

test1 %>% count(word, sort = TRUE) %>% filter(n >= 100) %>% print(n=100)
install.packages("textdata")
afinn <- get_sentiments("afinn")

prob12 <- inner_join(afinn, test1)
prob12 %>% nrow()
prob12 %>% filter(value >= 0) %>% nrow()
prob12 %>% nrow()
prob12 %>% filter(value == 4) %>% nrow()
