setwd("C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/clusters_consommateurs")
bilan = read.csv("table_analyse_3.csv", sep = ",",header=T)

library(dplyr)
library(cluster)
library(fpc)
library("ggplot2")
library("reshape2")
library("purrr")
library("dplyr")# let's start with a dendrogram
library("dendextend")

#on ne prends pas les indiviuds agés de moins de 18 ans
bilan2 <- filter(bilan, tage > 3)


col = colnames(bilan)

#toutes les colonnes sauf nomen as factor

bilan$sexeps<- as.factor(bilan$sexeps)
bilan$tage<- as.factor(bilan$tage)
bilan$bmi<- as.factor(bilan$bmi)
bilan$fromages<- as.factor(bilan$fromages)
bilan$fruits<- as.factor(bilan$fruits)
bilan$lÃ.gumes..hors.pommes.de.terre.<- as.factor(bilan$lÃ.gumes..hors.pommes.de.terre.)
bilan$poissons<- as.factor(bilan$poissons)
bilan$ultra.frais.laitier<- as.factor(bilan$ultra.frais.laitier)
bilan$viande<- as.factor(bilan$viande)
bilan$volaille.et.gibier<- as.factor(bilan$volaille.et.gibier)

#  "nomen"                           "sexeps"                          "tage"                            "bmi"                            
#  "fromages"                        "fruits"                          "lÃ.gumes..hors.pommes.de.terre." "poissons"                       
#  "ultra.frais.laitier"             "viande"                          "volaille.et.gibier"              

#calcul matrice des distances
gower.dist <- daisy(bilan[ ,2:11], metric = c("gower"))

# Clustering ascendant
aggl.clust.c <- hclust(gower.dist, method = "complete")
plot(aggl.clust.c, main = "Agglomerative, complete linkages")

# Analyse des clusters
cstats.table <- function(dist, tree, k) {
  clust.assess <- c("cluster.number","n","within.cluster.ss","average.within","average.between",
      "wb.ratio","dunn2","avg.silwidth")
  clust.size <- c("cluster.size")
  stats.names <- c()
  row.clust <- c()
  
  output.stats <- matrix(ncol = k, nrow = length(clust.assess))
  cluster.sizes <- matrix(ncol = k, nrow = k)
  
  for(i in c(1:k)){
    row.clust[i] <- paste("Cluster-", i, " size")
  }
  
  for(i in c(2:k)){
    stats.names[i] <- paste("Test", i-1)
    
    for(j in seq_along(clust.assess)){
      output.stats[j, i] <- unlist(cluster.stats(d = dist, clustering = cutree(tree, k = i))[clust.assess])[j]
    }
    
    for(d in 1:k) {
      cluster.sizes[d, i] <- unlist(cluster.stats(d = dist, clustering = cutree(tree, k = i))[clust.size])[d]
      dim(cluster.sizes[d, i]) <- c(length(cluster.sizes[i]), 1)
      cluster.sizes[d, i]
      
    }
  }
  
  output.stats.df <- data.frame(output.stats)
  
  cluster.sizes <- data.frame(cluster.sizes)
  cluster.sizes[is.na(cluster.sizes)] <- 0
  
  rows.all <- c(clust.assess, row.clust)
  # rownames(output.stats.df) <- clust.assess
  output <- rbind(output.stats.df, cluster.sizes)[ ,-1]
  colnames(output) <- stats.names[2:k]
  rownames(output) <- rows.all
  
  is.num <- sapply(output, is.numeric)
  output[is.num] <- lapply(output[is.num], round, 2)
  
  output
}


stats.df.divisive <- cstats.table(gower.dist, divisive.clust, 7)
stats.df.divisive

stats.df.aggl <-cstats.table(gower.dist, aggl.clust.c, 7) #complete linkages looks like the most balanced approach
stats.df.aggl

#------------------------------choisir le nb de clusters --------------------------------

ggplot(data = data.frame(t(cstats.table(gower.dist, aggl.clust.c, 12))),
       aes(x=cluster.number, y=within.cluster.ss)) +
  geom_point()+
  geom_line()+
  ggtitle("Agglomerative clustering") +
  labs(x = "Num.of clusters", y = "Within clusters sum of squares (SS)") +
  theme(plot.title = element_text(hjust = 0.5))


ggplot(data = data.frame(t(cstats.table(gower.dist, aggl.clust.c, 12))),
       aes(x=cluster.number, y=avg.silwidth)) +
  geom_point()+
  geom_line()+
  ggtitle("Agglomerative clustering") +
  labs(x = "Num.of clusters", y = "Average silhouette width") +
  theme(plot.title = element_text(hjust = 0.5))

#------------------------------ dendro --------------------------------------------------

dendro <- as.dendrogram(aggl.clust.c)

dendro.col <- dendro %>%
  set("branches_k_color", k = 10, value = c("darkslategray3", "gold3", "darkslategray4", "cyan3", "gold3", "darkslategray", "darkslategray4", "gold3",  "darkslategray4", "cyan3")) %>%
  set("branches_lwd", 0.6) %>%
  set("labels_colors", value = c("darkslategray")) %>%
  set("labels_cex", 0.5)

ggd1 <- as.ggdend(dendro.col)

ggplot(ggd1, theme = theme_minimal()) +
  labs(x = "Num. observations", y = "Height", title = "Dendrogram, k = 10")


clust.num <- cutree(aggl.clust.c, k = 10)
bilan.cl <- cbind(bilan, clust.num)

#write.table(bilan.cl, "clusters_enf.csv", sep = ";", row.names = TRUE)
