#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:23:25 2023

@author: blahner
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

root = os.path.join("/home", "blahner", "projects", "precise-eyedrop") #your path to project root
save_path = os.path.join(root, "exp4_hitormiss", "output")
data_path = os.path.join(root, "exp4_hitormiss", "data")

if not os.path.exists(save_path):
    os.makedirs(save_path)

is_save=True
data = pd.read_excel(os.path.join(data_path, "head_tilt_data.xlsx"))
data = data.iloc[:,:11] #discard the comments that were included in the xcel file

angle_truth = [16.4, 35.59] #based on calculations from code in "delivery_model" folder

plt.figure
plt.plot(data.loc[:,"Angle"], np.mean(data.iloc[:,1:],axis=1))
plt.vlines(angle_truth, 0, 1, color='red',linestyle='dashed')
plt.hlines(1.0, angle_truth[0], angle_truth[1], color='red', linestyle='dashed')
plt.xlabel("Head Tilt Angle (degrees)")
plt.ylabel("Mean Hit Rate")
if is_save:
    plt.savefig(os.path.join(save_path, "neckext_plot.svg"))
    plt.savefig(os.path.join(save_path, "neckext_plot.png"))
plt.show()

print("exited script with no errors")