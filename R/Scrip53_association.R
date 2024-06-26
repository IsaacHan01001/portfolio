library(dslabs)
library(tidyverse)
data("research_funding_rates")

totals <- research_funding_rates %>% 
  select(-discipline) %>% 
  summarize_all(funs(sum)) %>% 
  summarize(yes_men = awards_men, 
            no_men = applications_men - awards_men,
            yes_women = awards_women,
            no_women = applications_women - awards_women)
totals %>% summarize(percent_men = yes_men/(yes_men + no_men),
                     percent_women = yes_women/(yes_women + no_women))


# Lady Tasting Tea problem ------------------------------------------------
#Fischer's Exact Test

tab <- matrix(c(3,1,1,3),2,2)
rownames(tab) <- c("Poured Before", "Poured After")
colnames(tab) <- c("Guessed Before", "Guessed After")
tab

fisher.test(tab, alternative ='greater')


# Chi-squared test --------------------------------------------------------

funding_rate <- totals %>% summarize(percent_total = (yes_men + yes_women)/
                                       (yes_men+no_men+yes_women+no_women)) %>% 
  .$percent_total
funding_rate

two_by_two <- tibble(awarded = c("no","yes"),
                     men = c(totals$no_men, totals$yes_men),
                     women = c(totals$no_women, totals$yes_women))
two_by_two


tibble(awarded = c('no','yes'),
       men = (totals$no_men + totals$yes_men)*c(1-funding_rate, funding_rate),
       women = (totals$no_women + totals$yes_women)*c(1-funding_rate, funding_rate))

two_by_two %>% select(-awarded) %>% chisq.test()

# odd calculation ---------------------------------------------------------

odds_men <- (two_by_two$men[2] / sum(two_by_two$men))/
  (two_by_two$men[1] / sum(two_by_two$men))
odds_men

odds_women <- (two_by_two$women[2] / sum(two_by_two$women))/
  (two_by_two$women[1] / sum(two_by_two$women))
odds_women

odds_men/odds_women

# -------------------------------------------------------------------------

two_by_two %>% 
  select(-awarded) %>% 
  mutate(men = men*10, women = women*10) %>% 
  chisq.test()
 