x <- c('tidyverse', 'readr', 'stringr')
lapply(x, require, character.only = TRUE)

results <- read_csv('/Users/tompreston/program/scrape/Untitled Folder/results.csv', col_names = FALSE)

colnames(results) <- c('surname', 'firstname', 'country', 'div_rank', 'gen_rank', 'ovr_rank', 'swim', 'bike', 'run', 'total', 'points', 'partial_link')
results_n <- results %>%
  mutate(sn = str_extract(surname, '(?<=|)([a-zA-Z]+)'))
# results
results_n$sn

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}
# Each section and total histograms ---------
sw <- ggplot(results) +
  geom_histogram(aes(swim)) +
  labs(title = "Swim")

bk <- ggplot(results) +
  geom_histogram(aes(bike)) +
  labs(title = "Bike")

rn <- ggplot(results) +
  geom_histogram(aes(run)) +
  labs(title = "Run")

tot <- ggplot(results) +
  geom_histogram(aes(total)) +
  labs(title = "Total")

multiplot(sw, bk, rn, tot, cols = 2)

# Each section and total boxplots ---------
sw <- ggplot(results) +
  geom_boxplot(aes(swim)) +
  labs(title = "Swim")

bk <- ggplot(results) +
  geom_boxplot(aes(bike)) +
  labs(title = "Bike")

rn <- ggplot(results) +
  geom_boxplot(aes(run)) +
  labs(title = "Run")

tot <- ggplot(results) +
  geom_boxplot(aes(total)) +
  labs(title = "Total")

multiplot(sw, bk, rn, tot, cols = 2)

