




library(magrittr)
library(dplyr)
library(ggplot2)
library(plotly)
library(data.table)

setwd("C:/Users/agaca/Documents/GitHub/recommandations_alimentation")
options(scipen=999)

#################
## DATA IMPORT ##
#################

nomenclature = read.csv("Base_a_analyser/nomenclature.csv", sep = ";", colClasses = c("character"))
consommation = read.csv("Base_a_analyser/consommation.csv", sep = ",", colClasses = c("character")) 
individu = read.csv("Base_a_analyser/individu.csv", sep = ";", colClasses = c("character"))
repas = read.csv("Base_a_analyser/repas.csv", sep = ";", colClasses = c("character"))

#######################
## DATA MANIPULATION ##
#######################

#####################################################
## CONSTRUCTION BASE POUR L'ANALYSE MOTIF FR?QUENT ##
#####################################################

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


################################
## BASE INVERSÉE DES ALIMENTS ##
################################


apc_aliment = consommation %>%
  filter(codgr != "45") %>% #enleve 71 lignes d'aliment non identifiés
  mutate(qte_nette = as.numeric(qte_nette)) %>%
  group_by(nomen, tyrep, codal) %>%
  summarise(nbre_consom = n(),
            qte_moyenne = round(mean(qte_nette, na.rm = TRUE), 2)) %>%
  filter(!is.na(qte_moyenne)) %>% #enleve 
  ungroup() %>%
  inner_join(individu %>%
               select(nomen, sexe_ps, v2_age, poidsm, taille, bmi, regimem) %>%
               distinct() %>%
               filter(bmi != ""), by = "nomen") %>%
  mutate(regimem = ifelse(regimem == "", "0", regimem)) %>%
  select(-nomen) %>%
  arrange(qte_moyenne)



#write.table(apc_aliment, "Base à analyser/apc_aliment.csv", sep = ";", row.names = FALSE)



###
## BASE CONSOMMATEUR
###

repas_consommateur = repas %>%
  select(nomen, duree, avecqui) %>%
  mutate(avecqui = ifelse(avecqui == "1", "seul",
                          ifelse(avecqui %in% c("2", "3"), "accompagne", "avecqui.3"))) %>%
  group_by(nomen) %>%
  mutate(duree = sum(as.numeric(duree), na.rm = TRUE)) %>%
  filter(avecqui != "avecqui.3") %>%
  group_by(nomen, duree, avecqui) %>%
  summarise(eff = n()) %>%
  tidyr::spread(key = avecqui, value = eff) %>%
  ungroup() %>%
  mutate_all(~replace(., is.na(.), 0))




comportement_consommateur = consommation %>%
  select(nomen, codgr, qte_nette) %>%
  full_join(distinct(select(nomenclature, codgr, libgr)), by = "codgr") %>%
  filter(codgr != "45") %>% #code non identifié
  select(-codgr) %>%
  mutate(qte_nette = as.numeric(qte_nette)) %>%
  group_by(nomen, libgr) %>%
  summarise(qte = sum(qte_nette)) %>%
  tidyr::spread(key = libgr, value = qte) %>%
  ungroup() %>%
  mutate_all(~replace(., is.na(.), 0)) %>%
  left_join(repas_consommateur, by = "nomen") %>%
  left_join(select(individu, nomen, sexe_ps, v2_age, bmi), by = "nomen")

comportement_consommateur = comportement_consommateur[, !grepl( "autres" , names(comportement_consommateur) )]

write.table(comportement_consommateur, "BDD/Base_a_analyser/comportement_consommateur.csv", sep = ";", row.names = FALSE)
