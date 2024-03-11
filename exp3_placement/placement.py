#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 20:29:35 2023

@author: blahner
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import seaborn as sns
import numpy as np
import scipy.io as sio

root = os.path.join("/home", "blahner", "projects", "precise-eyedrop") #your path to project root
save_path = os.path.join(root, "exp3_placement", "output")
data_path = os.path.join(root, "exp3_placement", "data")

if not os.path.exists(save_path):
    os.makedirs(save_path)

is_save=True
data = pd.read_excel(os.path.join(data_path, "parameter_verification.xlsx"))

#this file contains predicted hit or miss for many pairs of (x, z) bottle tip placement.
#used just to overlay patch on plot, not essential to results.
tmp = sio.loadmat(os.path.join(data_path, "angle25validf_d.mat")) 
tmp_results = tmp['results']
bounds = {"x": [], "z": [], "hit": []}
for r in range(tmp_results.shape[0]):
    bounds["x"].append(tmp_results[r,:][0][0][0])
    bounds["z"].append(tmp_results[r,:][0][0][1] - 5) #minus 5 because we are now centering the z at the center of eye, not bottom eyelid
    bounds["hit"].append(bool(tmp_results[r,:][0][0][2]))

df_theory = pd.DataFrame(bounds)
idx = (df_theory["hit"] == True).values
df_hits = df_theory.iloc[idx,:2]

df_bottom = df_hits.iloc[(df_hits["z"] == np.min(df_hits["z"])).values,:]
df_top= df_hits.iloc[(df_hits["z"] == np.max(df_hits["z"])).values,:]
df_leftax = df_hits.iloc[(df_hits["x"] == np.min(df_hits["x"])).values,:]

la = tuple(df_leftax.iloc[np.argmax(df_leftax["z"]),:])

ll = tuple(df_bottom.iloc[np.argmin(df_bottom["x"]) ,:]) #lower left
lr = tuple(df_bottom.iloc[np.argmax(df_bottom["x"]) ,:])#lower right

ul = tuple(df_top.iloc[np.argmin(df_top["x"]) ,:]) #upper left
ur = tuple(df_top.iloc[np.argmax(df_top["x"]) ,:]) #upper right

#where we actually designed the device to place the bottle tip
x_truth = 5 #in mm
y_truth = 0 #in mm
z_truth = 12 #in mm

ax = sns.scatterplot(data=data, x="x",y="z")
plt.plot(x_truth, z_truth, color = 'red', marker='o')
ax.add_patch(patches.Polygon([la, ll, lr, ur, ul], fill=True, alpha=0.2, color='red'))

if is_save:
    plt.savefig(os.path.join(save_path, "parameterverification_scatterplot.svg"))
    plt.savefig(os.path.join(save_path, "parameterverification_scatterplot.png"))
plt.show()
plt.clf()