

library(magrittr)
library(dplyr)
library(ggplot2)
library(plotly)

setwd("D:/APT/3e_annee/Projet fil rouge/BDD/")


#################
## DATA IMPORT ##
#################

nomenclature = read.csv("Base à analyser/nomenclature.csv", sep = ";", colClasses = c("character"))
consommation = read.csv("Base à analyser/consommation.csv", sep = ";", colClasses = c("character")) 
individu = read.csv("Base à analyser/individu.csv", sep = ";", colClasses = c("character"))
repas = read.csv("Base à analyser/repas.csv", sep = ";", colClasses = c("character"))

# modification de la base individu
individu = individu %>%
  mutate(sexe = ifelse(sexe_ps == 1, "Homme", "Femme"),
         class_age = factor(class_age, levels = c("enfant", "jeune adulte", "adulte", "personne agee")))
  

########################
## DATA VISUALISATION ##
########################


# A, La distribution d'individus de chaque catégorie de consommateurs
#####################################################################

# Graphique
###########

ggplotly(
  ggplot(individu %>%
           group_by(sexe, class_age) %>%
           summarise(eff = n()) %>%
           ungroup(), aes(x = class_age, y = eff)) +
    geom_bar(stat = "identity", fill = "cornflowerblue", alpha = .7) +
    labs(title = "Distribution du nombre d'individu par catégorie de consommateurs",
         x = "Catégories d'âge",
         y = "Nombre d'individu") +
    facet_grid(sexe~., scales = "free") +
    scale_y_continuous(breaks = seq(0, 900, 100)) +
    theme_bw() +
    theme(plot.title = element_text(size = rel(1.8), face = "bold", hjust = .5),
          strip.text.y = element_text(size = rel(1.8), face = "bold"),
          axis.title = element_text(size = rel(1.5), face = "bold"),
          axis.text = element_text(size = rel(1.4)))
) %>%
  layout(margin = list(b = 70, l = 95, t = 80))


# B, La distribution de repas de chaque catégorie de consommateurs
##################################################################

# 1, Data
##########

distri_repas = consommation %>%
  filter(codgr != 45) %>%
  select(nomen, nojour, tyrep) %>%
  distinct() %>%
  full_join(distinct(select(individu, nomen, id_categorie, sexe, class_age)), by = "nomen") %>%
  full_join(data.frame(tyrep = c("1", "2", "3", "4", "5", "6"),
                       type_repas = c("petit-déjeuner", "collation matin", "déjeuner", "collation aprèm", "diner", "collation soir")) %>%
              mutate(tyrep = as.character(tyrep)), by = "tyrep") %>%
  select(-tyrep) %>%
  group_by(id_categorie, sexe, class_age, type_repas) %>%
  summarize(eff = n()) %>%
  group_by(id_categorie, sexe, class_age) %>%
  mutate(pourcentage = round(100*eff/sum(eff), 2)) %>%
  ungroup()

# 2, Graphique
##############

# a, Nombre de repas observé par catégorie de consommateurs
ggplotly(
  ggplot(distri_repas %>%
           group_by(id_categorie, sexe, class_age) %>%
           summarise(eff = sum(eff)/1000),
         aes(x = class_age, y = eff)) +
    geom_bar(stat = "identity", fill = "cornflowerblue", alpha = .7) +
    facet_grid(sexe~., scales = "free_x") +
    labs(title = "Distribution du nombre de repas par catégorie de consommateurs",
         x = "Catégories d'âge",
         y = "Nombre de repas observé (k repas)") +
    scale_y_continuous(breaks = seq(0, 25, 5)) +
    theme_bw() +
    theme(plot.title = element_text(size = rel(1.8), face = "bold", hjust = .5),
          strip.text.y = element_text(size = rel(1.8), face = "bold"),
          axis.title = element_text(size = rel(1.5), face = "bold"),
          axis.text = element_text(size = rel(1.4)))
) %>%
  layout(margin = list(b = 70, l = 120, t = 80))


# b, Nombre de repas observé par catégorie de consommateurs et par type de repas
ggplotly(
  ggplot(distri_repas %>%
           mutate(type_repas = factor(type_repas, levels = c("petit-déjeuner", "collation matin", "déjeuner", "collation aprèm", "diner", "collation soir"))),
         aes(x = type_repas, y = eff/100, fill = type_repas)) +
    geom_bar(stat = "identity") +
    facet_grid(sexe ~ class_age) +
    labs(title = "Nombre de repas par catégorie et par type de repas",
         x = "Type de repas",
         y = "Nombre de repas*0.01") +
    scale_y_continuous(breaks = seq(0, 60, 5)) +
    theme_bw() +
    theme(plot.title = element_text(size = rel(1.8), face = "bold", hjust = .5),
          strip.text = element_text(size = rel(1.8), face = "bold"),
          axis.title = element_text(size = rel(1.5), face = "bold"),
          axis.text.x = element_blank(),
          axis.ticks.x = element_blank(),
          axis.text.y = element_text(size = rel(1.5)),
          legend.title = element_blank(),
          legend.text = element_text(size = rel(1.5)),
          legend.background = element_rect(fill = alpha("white", 0.001))) 
) %>%
  layout(margin = list(b = 70, l = 115, t = 100))
 


# C, Aliments par catégorie de consommateurs et par type de repas
##################################################################

# 1, Data
##########
top10_aliment_cat_tyrep = consommation %>%
  full_join(distinct(select(nomenclature, codgr, group_alim)), by = "codgr") %>%
  filter(codgr != 45) %>%
  select(nomen, nojour, tyrep, group_alim) %>%
  full_join(distinct(select(individu, nomen, id_categorie, sexe, class_age)), by = "nomen") %>%
  full_join(data.frame(tyrep = c("1", "2", "3", "4", "5", "6"),
                       type_repas = c("petit-déjeuner", "collation matin", "déjeuner", "collation aprèm", "diner", "collation soir")) %>%
              mutate(tyrep = as.character(tyrep)), by = "tyrep") %>%
  mutate(type_repas = factor(type_repas, levels = c("petit-déjeuner", "collation matin", "déjeuner", "collation aprèm", "diner", "collation soir"))) %>%
  group_by(sexe, class_age, type_repas, group_alim) %>%
  summarise(eff = n()) %>%
  arrange(desc(eff)) %>%
  top_n(n = 10, eff) %>%
  arrange(sexe, class_age, type_repas) %>%
  ungroup()


# 2, Graphique
##############
ggplot(top10_aliment_cat_tyrep, aes(y = group_alim, x = eff, col = type_repas, fill = type_repas, size = eff)) +
  geom_point() +
  labs(title = "Top 10 aliments consommés par catégorie de consommateurs et par type de repas",
       x = "Nombre total de fois de consommation",
       y = "Groupe d'aliments") +
  facet_grid(sexe ~ class_age, scales = "free_x") +
  scale_x_continuous(breaks = seq(0, 5000, 500)) +
  theme_bw() +
  theme(plot.title = element_text(size = rel(1.5), face = "bold", hjust = .5),
        strip.text = element_text(size = rel(1.3), face = "bold"),
        axis.title = element_text(size = rel(1.5), face = "bold"),
        axis.text.x = element_text(size = rel(1.3), face = "bold", angle = 30, margin = margin(t = 5)),
        axis.text.y = element_text(size = rel(1.2), face = "bold"),
        legend.title = element_blank(),
        legend.text = element_text(size = rel(1.3)),
        legend.background = element_rect(fill = alpha("white", 0.001)),
        plot.margin = margin(b = 20, l = 20, t = 15),
        panel.spacing = unit(1, "lines"))


