require(data.table)
require(ggplot2)

source("~/Documents/isentium/signal/Rcode/ref.R")

setwd("/Users/admin/Dropbox/Projects/game AI/crossword/results/")
fs <- list.files()

rs <- list()
for (i in 1:length(fs)) {
  rs[[i]] <- read.csv(fs[i], sep="\t", header=F,
                      col.names=c("i","clue","word","n","day","year","fname","x","prompt","guess","win","t","user"))
}
rs <- ListToDataFrame(rs)

rs$t.adj <- rs$t - rs$n/7
rs$day.name <- ""
rs$day.name[rs$day == 0] <- "6_Sun"; rs$day.name[rs$day == 1] <- "0_Mon"; rs$day.name[rs$day == 2] <- "1_Tue"; 
rs$day.name[rs$day == 3] <- "2_Wed"; rs$day.name[rs$day == 4] <- "3_Thu"; rs$day.name[rs$day == 5] <- "4_Fri"; rs$day.name[rs$day == 6] <- "5_Sat";
rs$day.adj <- 0
rs$day.adj[rs$day == 0] <- 4; rs$day.adj[rs$day == 1] <- 1; rs$day.adj[rs$day == 2] <- 2; 
rs$day.adj[rs$day == 3] <- 3; rs$day.adj[rs$day == 4] <- 5; rs$day.adj[rs$day == 5] <- 6; rs$day.adj[rs$day == 6] <- 7;
rs$win.10 <- 1
rs$win.10[rs$win == "false"] <- 0

p1 <- ggplot(rs[win == "true"], aes(x=n+x/10, y=log(t.adj), group=n+x/10)) + 
  geom_boxplot() + geom_point() + ggtitle("correct") + xlab("word length + (letters completed)/10") + ylab("log(typing-adjusted time)")
p2 <- ggplot(rs[win == "true"], aes(x=n+x/10, y=log(t.guess), group=n+x/10)) + 
  geom_boxplot() + geom_point() + ggtitle("incorrect") + xlab("word length + (letters completed)/10") + ylab("log(typing-adjusted time)")
multiplot(plotlist=list(p1, p2))

ggplot(rs, aes(x=day.name, y=log(t.adj), group=day.name, color=day.name)) + 
  geom_boxplot() + ggtitle("time by day of week") + xlab("day of week") + ylab("log(typing-adjusted time)")

ggplot(rs, aes(x=n, y=log(t.adj), group=paste(n, win), color=win)) + 
  ggtitle("time vs word length") + xlab("word length") + ylab("log(typing-adjusted time)") +
  geom_point() + geom_boxplot()


by.n.x.day <- aggregate(list(p.win=rs$win.10), by=list(n=rs$n, x=rs$x, day.adj=rs$day.adj), FUN=mean)
fit <- lm(p.win ~ n + x + day.adj, data=by.n.x.day)
summary(fit)
by.n.x.day$p.win.guess <- 0.728 - 0.054 * by.n.x.day$n + 0.128 * by.n.x.day$x - 0.037 * by.n.x.day$day.adj

fit <- lm(t.adj ~ n + x + day.adj, data=rs)
summary(fit)
rs$t.guess <- 0.473 + 1.142 * rs$n - 1.449 * rs$x + 0.544 * rs$day.adj