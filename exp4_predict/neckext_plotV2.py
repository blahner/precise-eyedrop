#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:23:25 2023

@author: blahner
"""

import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import scipy


#plot the ball-in-tube feedback mechanism
root = '/Users/blahner/Documents/Python/ocular275/neckextension'
is_save=False
data_path = os.path.join(root, 'data')
save_path = os.path.join(root, 'plots')
data = pd.read_excel(os.path.join(data_path,  "head tilt v3.xlsx")) #"head_tilt_accuracy_x4_y0_z12.xlsx"))

data = data.iloc[:,:11] #discard the comments that were included in the xcel file

angle_truth = [16.4, 35.59] #based on matlab calculations

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
#perform stats
