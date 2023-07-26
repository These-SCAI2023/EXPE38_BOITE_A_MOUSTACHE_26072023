#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:18:15 2023

@author: obtic2023
"""
import json
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        texte =json.load(json_data)
    return texte
tableau={}
liste_auteur=[]
liste_version_spacy=[]
liste_config=[]
liste_dist=[]
liste_auteur=[]
liste_name_metric=[]
liste_version=[]



path_data="../DATA/ELTeC-Fra_spacy3.5.1_CONCAT_DISTANCES/*/*.json"

for path_autor in glob.glob(path_data):
    # print(path_autor)
    
    
    # for dist_file in glob.glob(f"{path_autor}/*.json"):
    # print(dist_file)
    distance=lire_fichier(path_autor)
    autor=path_autor.split("/")[4]
    autor=autor.split("_")[0]
    version=path_autor.split("/")[-1]
    version=version.split("_")[1]

    if version=="kraken-base":
        version=re.sub("kraken-base","kraken",version)
        print(version)
    
    liste_distance=[]
    for key, config in distance.items():
        
        for paire, resultats in config.items():
            if paire=="spacy-lg-concat--spacy-lg-concat":
                paire=re.sub("spacy-lg-concat--spacy-lg-concat","spaCy_lg",paire)
            if paire=="spacy-md-concat--spacy-md-concat":
                paire=re.sub("spacy-md-concat--spacy-md-concat","spaCy_md",paire)
            if paire=="spacy-sm-concat--spacy-sm-concat":
                paire=re.sub("spacy-sm-concat--spacy-sm-concat","spaCy_sm",paire)
            if "PP" in paire:
                paire=re.sub("PP","Réf",paire)
            
            
            
            for name_metric, liste in resultats.items():
                # print(liste)
                
                for r in liste:
                    if paire =="spaCy_lg" and name_metric=="cosinus":#or paire=="sm--sm" or paire=="md--md":
                        liste_name_metric.append(name_metric)
                        # liste_version.append(version)
                        liste_config.append(version+"--"+paire)
                        liste_auteur.append(autor)
                        # liste_version_spacy.append(version_spacy)
                        liste_dist.append(r)
            
                
    

tableau["Auteur"]=liste_auteur
# tableau["Version"]=liste_version
tableau["Configuration"]=liste_config
tableau["Distance"]=liste_dist
tableau["Metric"]=liste_name_metric
# tableau["Version_spacy"]=liste_version_spacy
data_tab = pd.DataFrame(tableau)


sns.set_theme(style="ticks")

# Initialize the figure with a logarithmic x axis
f, ax = plt.subplots(figsize=(7, 6))
ax.set_xscale("linear")

# Load the example planets dataset
# planets = sns.load_dataset("planets")

# Plot the orbital period with horizontal boxes
# sns.boxplot(x=data_tab.Distance[(data_tab.Metric=="cosinus") & (data_tab.Configuration=="kraken--lg--lg")],  y=data_tab.Configuration[data_tab.Configuration=="kraken--lg--lg"], data=data_tab,
#             whis=[0, 100], width=.6, palette="vlag")
sns.boxplot(x="Distance",  y="Configuration", data=data_tab,
            whis=[0, 1], width=.6, palette="vlag")

# Add in points to show each observation
# sns.stripplot(x=data_tab.Distance[(data_tab.Metric=="cosinus") & (data_tab.Configuration=="kraken--lg--lg")], y=data_tab.Configuration[data_tab.Configuration=="kraken--lg--lg"], data=data_tab,
#               size=4, color=".3", linewidth=0)
sns.stripplot(x="Distance", y="Configuration", data=data_tab,
              size=4, color=".3", linewidth=0)

# Tweak the visual presentation
ax.xaxis.grid(True)
ax.set(ylabel="")
sns.despine(trim=True, left=True)
plt.savefig("../DATA/DISTANCES_GRAPH/spacy-lg_cosinus.png",dpi=300, bbox_inches="tight")
 
 
 
 
 
 
 
 
 