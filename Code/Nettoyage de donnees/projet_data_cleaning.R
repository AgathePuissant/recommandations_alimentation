



library(magrittr)
library(dplyr)

setwd("C:/Users/agaca/Documents/GitHub/recommandations_alimentation")


###################
## DATA CLEANING ##
###################



# BASE BRUTE
nomenclature = read.csv("Base brute/Nomenclature_3.csv", sep = ";", colClasses = c("character"))
#consommation = read.csv("Base brute/Table_conso.csv", sep = ";", colClasses = c("character"))
individu = read.csv("Base brute/Table_indiv.csv", sep = ";", colClasses = c("character"))
#repas = read.csv("Base brute/Table_repas.csv", sep = ";", colClasses = c("character"))
#menage = read.csv("Base brute/Table_menage_1.csv", sep = ";", colClasses = c("character"))


# BASE FINALE
individu = individu %>%
  select(nomen, sexe_ps, v2_age, poidsm, taille, bmi, opipoids, situ_prof, situ_mat, statnut, pays_nai, region, aptotal_hebdo, aptotal_met, enceinte, regimem, autreg_cod) %>%
  mutate(class_age = ifelse(v2_age <= 17, 'enfant',
                            ifelse(v2_age <= 35, 'jeune adulte',
                                   ifelse(v2_age <= 60, 'adulte', 'personne agee')))) %>%
  mutate(id_categorie = group_indices(individu, sexe_ps, class_age))


nomenclature = nomenclature %>%
  full_join(nomenclature %>%
              select(codgr, libgr) %>%
              distinct() %>%
              mutate(group_alim = c("pain", "c�r�ales pdj", "p�tes",
                                    "riz et bl�", "autres c�r�ales", "viennoiserie",
                                    "biscuits", "p�tisseries", "lait",
                                    "produit laitier", "fromages", "oeufs",
                                    "beurre", "huile", "margarine",
                                    "autres graisses", "viande", "volaille",
                                    "abats", "charcuterie", "poissons",
                                    "crustac�s et mollusques", "l�gumes", "pommes de terre",
                                    "l�gumes secs", "fruits", "fruits secs",
                                    "glaces", "chocolat", "sucres",
                                    "eaux", "boissons sans alcool", "alcool",
                                    "caf�", "boissons chaudes", "pizzas",
                                    "sandwichs", "soupes", "plats compos�s",
                                    "entremets", "compotes", "condiments",
                                    "aliments particuliers", "-" )), by = c("codgr", "libgr")) %>%
  mutate(libsougr = ifelse(sougr == "99", libgr, libsougr))


write.table(individu, "Base � analyser/individu.csv", sep = ";", row.names = FALSE)
write.table(nomenclature, "Base � analyser/nomenclature.csv", sep = ";", row.names = FALSE)

