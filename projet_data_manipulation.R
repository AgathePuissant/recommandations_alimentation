




library(magrittr)
library(dplyr)
library(ggplot2)
library(plotly)
library(data.table)

setwd("D:/APT/3e_annee/Projet fil rouge/BDD/")
options(scipen=999)

#################
## DATA IMPORT ##
#################

nomenclature = read.csv("Base à analyser/nomenclature.csv", sep = ";", colClasses = c("character"))
consommation = read.csv("Base à analyser/consommation.csv", sep = ";", colClasses = c("character")) 
individu = read.csv("Base à analyser/individu.csv", sep = ";", colClasses = c("character"))
repas = read.csv("Base à analyser/repas.csv", sep = ";", colClasses = c("character"))

#######################
## DATA MANIPULATION ##
#######################

#####################################################
## CONSTRUCTION BASE POUR L'ANALYSE MOTIF FRÉQUENT ##
#####################################################

#  motifs fréquents de groupe d'aliment
prep_conso_pattern <- function(echelle) {
  
  "La fonction qui crée la base pour l'analyse de motif fréquent par groupe d'aliement ou par sous-groupe d'aliment.
  
  Les filtres appliqués :
  + Enlever la collation du matin et celle du soir
  + Enlever les repas d'un seul aliment
  
  INPUT :
  + echelle : 'groupe' si l'analyse est basée sur groupe d'aliment
              'sous-groupe' si l'analyse est basée sur sous-groupe d'aliment -- str
  
  OUPUT :
  + Base de données dont les colonnes sont les groupes / sous-groupes d'aliments et les lignes sont les types de repas de chaque individu :
      + 1 : si le groupe / sous-groupe d'aliment est consommé
      + 0 : sinon"
  
  if (echelle == "groupe") {
    
    data = consommation %>%
      select(nomen, nojour, tyrep, codgr) %>%
      full_join(distinct(select(nomenclature, codgr, libgr)), by = "codgr") %>%
      filter(codgr != "45", #code non identifié
             tyrep %in% c("1", "3", "4", "5")) %>% #garder que le petit-déjeuner, le déjeuner et le diner
      select(-codgr) %>%
      group_by(nomen, nojour, tyrep) %>%
      filter(n() > 1 ) %>% #enlever les repas d'un aliment
      group_by(nomen, nojour, tyrep, libgr) %>%
      summarise(eff = 1) %>%
      tidyr::spread(key = libgr, value = eff) %>%
      ungroup() %>%
      mutate_all(~replace(., is.na(.), 0)) %>%
      full_join(distinct(select(individu, nomen, id_categorie)), by = "nomen") %>%
      left_join(distinct(select(repas, nomen, nojour, tyrep, avecqui)), by = c("nomen", "nojour", "tyrep"))
    
  } else if (echelle == "sous-groupe") {
    
    data = consommation %>%
      select(nomen, nojour, tyrep, codgr, sougr) %>%
      full_join(distinct(select(nomenclature, codgr, sougr, libsougr)), by = c("codgr", "sougr")) %>%
      filter(codgr != "45", #code non identifié
             tyrep %in% c("1", "3", "4", "5")) %>% #garder que le petit-déjeuner, le déjeuner et le diner
      select(- c(codgr, sougr)) %>%
      group_by(nomen, nojour, tyrep) %>%
      filter(n() > 1 ) %>% #enlever les repas d'un d'aliment
      group_by(nomen, nojour, tyrep, libsougr) %>%
      summarise(eff = 1) %>%
      tidyr::spread(key = libsougr, value = eff) %>%
      ungroup() %>%
      mutate_all(~replace(., is.na(.), 0)) %>%
      left_join(distinct(select(individu, nomen, id_categorie)), by = "nomen") %>%
      left_join(distinct(select(repas, nomen, nojour, tyrep, avecqui)), by = c("nomen", "nojour", "tyrep"))
    
  }
  data
}

conso_pattern_grp = prep_conso_pattern(echelle = "groupe")
conso_pattern_sougr = prep_conso_pattern(echelle = "sous-groupe")

#write.table(conso_pattern_grp, "Base à analyser/conso_pattern_grp.csv", sep = ";", row.names = FALSE) 
#write.table(conso_pattern_sougr, "Base à analyser/conso_pattern_sougr.csv", sep = ";", row.names = FALSE)

