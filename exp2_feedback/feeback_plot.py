#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 20:04:22 2023

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

root = '/Users/blahner/Documents/Python/ocular275/feedback'
is_save=True
data_path = os.path.join(root, 'data')
save_path = os.path.join(root, 'plots')
data = pd.read_excel(os.path.join(data_path, "FeedbackV2.xlsx"))

angle_truth = data.loc[0,"Angle of the feedback "]

observations = data.loc[:,"Head tilt"].values

#plot results
ax = sns.boxplot(observations)
sns.stripplot(observations, edgecolor='black', linewidth=2)
ax.axhline(angle_truth, color='red',linestyle='--')
plt.xlabel("Position")
plt.ylabel("Angle (degrees)")
plt.ylim([20, 32])
if is_save:
    plt.savefig(os.path.join(save_path, "feedback_boxplotV2.svg"))
    plt.savefig(os.path.join(save_path, "feedback_boxplotV2.png"))
plt.show()


#perform stats
res = scipy.stats.ttest_1samp(observations, popmean=angle_truth)
print("stats result:", res)
print("Feedback results")
print("mean = {}".format(observations.mean()))
print("STD = {}".format(np.std(observations)))
print("median = {}".format(np.median(observations)))
print("SEM = {}".format(observations.std()/np.sqrt(len(observations))))    