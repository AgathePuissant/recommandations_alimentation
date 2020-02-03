# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:49:29 2020

@author: lili-
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file="C:/Users/lili-/Desktop/PROJET_FIL_ROUGE/clusters_consommateurs/clusters_enf.csv"
clusters = pd.read_csv(file, sep = ";", encoding = 'latin-1')


def num_array(data, nom_col_cluster, nom_col_id, nb_clust, nb_labels, modalites):
    """
    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    nom_col_cluster : TYPE
        DESCRIPTION.
    nom_col_id : TYPE
        DESCRIPTION.
    nb_clust : TYPE
        DESCRIPTION.
    nb_labels : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    liste = [[] for i in range(nb_labels)]
    col = list(data.columns)
    col.remove(nom_col_id)
    col.remove(nom_col_cluster)
    compteur = 0
    for i in col :
        dati = list(clusters.groupby([i,nom_col_cluster]).count()[nom_col_id])
        for j in range(modalites[compteur]):
            liste[compteur] = dati[j*nb_clust:(j+1)*nb_clust]
            print(liste)
        compteur+=1
    #matrice = np.array(liste)
    return('matrice') 
        
## Clusters 4
# raw_data_4 = np.array([[7, 2, 0, 0],
#                        [762, 162, 132, 27],
#                        [1043,52, 387, 50],
#                        [135, 19, 102, 1],
#                        [249, 28, 145, 10],
#                        [575, 60, 166, 36],
#                        [592, 71, 73, 14],
#                        [261, 38, 33, 16],
#                        [60, 4, 34, 7],
#                        [950, 102, 376, 19],
#                        [802, 110, 109, 51],
#                        [952, 24, 354, 10],
#                        [887, 192, 165, 67],
#                        [740, 61, 471, 40],
#                        [1072, 155, 48, 37],
#                        [648, 195, 459, 10],
#                        [1164, 21, 60, 67],
#                        [697, 147, 407, 72],
#                        [1115, 69, 117, 5],
#                        [810, 101, 385, 16],
#                        [1002, 115, 134, 61],
#                        [906, 92, 249, 71],
#                        [906, 124, 270, 6],
#                        [885, 142, 273, 37],
#                        [927, 74, 246, 40]])

#taille_clust = [1812, 216, 519, 77]
    
raw_data_enf = np.array([[110, 270, 46, 0, 34, 432, 22, 181, 277, 92],
                        [471, 208, 35, 156, 78, 23, 38, 20, 52, 2],
                        [640, 313, 308, 14, 119, 34, 25, 35, 15, 29],
                        [22, 84, 7, 0, 7, 290, 12, 77, 26, 49],
                        [50, 100, 26, 0, 11, 77, 5, 67, 98, 22],
                        [32, 85, 11, 0, 16, 65, 5, 37, 153, 21],
                        [46, 110, 40, 14, 12, 1, 6, 20, 6, 2],
                        [138, 136, 62, 16, 33, 25, 6, 5, 9, 2],
                        [383, 148, 106, 24, 71, 9, 35, 25, 25, 11],
                        [366, 90, 96, 86, 54, 18, 11, 4, 18, 7],
                        [184, 38, 41, 30, 27, 4, 5, 1, 9, 9],
                        [68, 167, 42, 1, 26, 324, 23, 97, 70, 75],
                        [662, 357, 278, 64, 115, 141, 7, 135, 263, 13],
                        [491, 267, 69, 105, 90, 24, 55, 4, 11, 35],
                        [479, 463, 250, 33, 27, 261, 37, 152, 279, 64],
                        [742, 328, 139, 137, 204, 228, 48, 84, 65, 59],
                        [255, 708, 118, 32, 127, 338, 82, 131, 203, 47],
                        [966, 83, 271, 138, 104, 151, 3, 105, 141, 76],
                        [153, 732, 255, 105, 4, 430, 14, 121, 194, 39],
                        [1068, 59, 134, 65, 227, 59, 71, 115, 150, 84],
                        [460, 675, 126, 102, 105, 267, 48, 62, 269, 3],
                        [761, 116, 263, 68, 126, 222, 37, 174, 75, 120],
                        [420, 500, 261, 89, 147, 108, 19, 160, 288, 52],
                        [801, 291, 128, 81, 84, 381, 66, 76, 56, 71],
                        [375, 346, 339, 109, 178, 379, 11, 11, 234, 120],
                        [846, 445, 50, 61, 53, 110, 74, 225, 110, 3],
                        [393, 370, 332, 13, 199, 336, 80, 166, 123, 35],
                        [828, 421, 57, 157, 32, 153, 5, 70, 221, 88]])

taille_clust_enf = [1221, 791, 389, 170, 231, 489, 85, 236, 344, 123]


raw_data_8 = np.array([[2, 1, 1, 0, 3, 2, 0, 0],
              [395, 16, 300, 96, 236, 52, 387, 50],
              [29, 337, 104, 172, 120, 162, 132, 27],
              [58, 29, 24, 18, 6, 19, 102, 1],
              [58, 70, 38, 37, 46, 28, 145, 10],
              [133, 103, 135, 112, 92, 60, 166, 36],
              [132, 112, 122, 69, 157, 71, 73, 14],
              [45, 40, 86, 32, 58, 38, 33, 16],
              [30, 1, 9, 5, 15, 4, 34, 7],
              [184, 133, 229, 215, 189, 102, 376, 19],
              [212, 220, 167, 48, 155, 110, 109, 51],
              [302, 141, 238, 68, 176, 24, 354, 10],
              [124, 213, 167, 200, 183, 192, 165, 67],
              [262, 290, 100, 74, 14, 61, 471, 40],
              [164, 64, 305, 194, 345, 155, 48, 37],
              [216, 225, 90, 47, 70, 195, 459, 10],
              [210, 129, 315, 221, 289, 21, 60, 67],
              [179, 166, 109, 50, 193, 147, 402, 72],
              [247, 188, 296, 218, 166, 69, 117, 5],
              [117, 146, 178, 172, 197, 101, 385, 16],
              [309, 208, 227, 96, 162, 115, 134, 61],
              [212, 105, 361, 91, 137, 92, 249, 71],
              [214, 249, 44, 177, 222, 124, 270, 6],
              [387, 128, 78, 62, 230, 142, 273, 37],
              [39, 226, 327, 206, 129, 74, 246, 40]])

taille_clust = [426, 354, 405, 268, 359, 216, 519, 77]

def percentage (mat, tailles):
    dim = mat.shape
    nouvelle_mat = np.zeros(dim)
    for i in range(dim[0]):
        for j in range(len(tailles)):
            nouvelle_mat[i][j]=mat[i][j]/tailles[j]
    return(nouvelle_mat)

clusts = [1,2,3,4,5,6,7,8,9,10]

data_enf = percentage(raw_data_enf, taille_clust_enf)
data = percentage(raw_data_8, taille_clust)

labels = ["0","Homme","Femme",
          "3-10 ans","11-14 ans","15-17 ans","18-24 ans", "25-34 ans", "35-49 ans", "50-64 ans", "+65 ans",
          "Dénutrition-Maigreur","Normal-Surpoids", "Obésité",
          "Fromage -50", "Fromage +50",
          "Fruit -50", "Fruit +50",
          "Legumes -50", "Legumes +50",
          "Poisson -50", "Poisson +50",
          "Laitiers -50", "Laitiers +50",
          "Viande -50", "Viande +50",
          "Volaille -50", "Volaille +50"]

labels_ss = ["0","Homme","Femme",
          "Fromage -50", "Fromage +50",
          "Fruit -50", "Fruit +50",
          "Legumes -50", "Legumes +50",
          "Poisson -50", "Poisson +50",
          "Laitiers -50", "Laitiers +50",
          "Viande -50", "Viande +50",
          "Volaille -50", "Volaille +50"]


# nb_labels = len(labels)
# nb_clusts = len(clusts)
# modalites = [3,5,3,2,2,2,2,2,2,2]
# data = num_array(clusters, 'clust.num','nomen', 5, nb_labels,modalites)

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = plt.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

#heatmap(data, labels, clusts, cmap="magma_r", vmin=0, vmax=1)
heatmap(data_enf, labels, clusts, cmap="magma_r", vmin=0, vmax=1)

new_row = np.array([[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,0, 1, 1, 0, 0, 1]])
heatmap(new_row.T, labels, ['new'], cmap="magma_r", vmin=0, vmax=1)
