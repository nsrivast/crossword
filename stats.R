require(data.table)
require(ggplot2)

setwd("/Users/admin/Dropbox/Projects/game AI/crossword/")

r <- read.csv("results/ns_results2.txt", header=F, sep="\t",
              col.names=c("i_clue", "clue", "answer", "length", "day_of_week", 
                          "year", "puzpath", "n_fills", "prompt", "guess", "won", "time", "player_name"))

r <- data.table(r)
r.won <- r[won == "true"]
ggplot(r.won, aes(x=day_of_week, y=time)) + geom_point()