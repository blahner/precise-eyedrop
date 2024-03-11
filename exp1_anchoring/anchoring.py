#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:51:30 2023

@author: blahner
"""

import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import scipy.signal
import scipy.stats

root = os.path.join("/home", "blahner", "projects", "precise-eyedrop") #your path to project root
save_path = os.path.join(root, "exp1_anchoring", "output")
data_path = os.path.join(root, "exp1_anchoring", "data")

if not os.path.exists(save_path):
    os.makedirs(save_path)

"""
#columns in excel file: ['Time', 'Orientation_1', 'Orientation_2', 'Orientation_3',
       'Orientation_4', 'X_Accel_True', 'Y_Accel_True', 'Z_Accel_True',
       'Total_True', 'X_Accel_Raw', 'Y_Accel_Raw', 'Z_Accel_Raw', 'X_Gyro',
       'Y_Gyro', 'Z_Gyro', 'X_Mag', 'Y_Mag', 'Z_Mag', 'Button_Event']
100Hz sampling rate
"""
fs = 100.0 #sampling rate in Hz

cols_st = ["Subject","Trial","AvgXaccel_True","AvgYaccel_True","AvgZaccel_True","peak_freq","peak_amp","Device"]
steadiness_dict = {c: [] for c in cols_st}

bound_sec = 2.0 #boundary time in seconds of how long before and after to include in averaging analyses
bound_sr = bound_sec * fs

raw_plot_accel = True
raw_plot_norm = False #whether to plot the raw data or not
is_save = True
raw_accel_all_anchored = np.zeros((int(bound_sr*2 + 1),))
raw_accel_all_unanchored = np.zeros((int(bound_sr*2 + 1),))

subjects = ["Ben","Jesse","Carly","Seunghyeon"]
for sub in subjects:
    #get list of files
    filenames = glob.glob(os.path.join(data_path, sub + "*.xlsx"))
    assert(len(filenames) == 20) #20 files per subject
    
    for file in filenames:
        trial = int(file.split("trial_")[1].split(".")[0])
        if file.split(f"{sub}_")[1].split("_trial")[0] == "free":
            device = "Unanchored"
        elif file.split(f"{sub}_")[1].split("_trial")[0] == "constrained":
            device = "Anchored"
        else:
            print("Incorrect naming convention used for whether device was used or not")
            
        #Read in neck extension txt files and plot results
        print("Loading subject {} trial {}".format(sub, trial))
        data = pd.read_excel(os.path.join(data_path, file))
        beg = - np.inf
        end = np.inf
        squeeze = np.inf
        try:
            button_presses = np.where(data.loc[:,"Button_Event"] == 1)[0]
            if len(button_presses) > 1:
                squeeze = button_presses[-1] #take the last button press as true if the button was pressed more than once
            elif len(button_presses) == 1:
                squeeze = button_presses[0]
            else:
                print("No button press detected in subject {} trial {}.".format(sub,trial))
            beg = squeeze - bound_sr
            end = squeeze + bound_sr
            
            if beg < 0 or end > data.shape[0]:
                raise ValueError("Sampling bounds exceed the amount of data collected")
            
            #https://clinicalmovementdisorders.biomedcentral.com/articles/10.1186/s40734-020-00086-7#Sec2
            FOI = ["X_Accel_True","Y_Accel_True","Z_Accel_True"] #["X_Accel_Raw","Y_Accel_Raw","Z_Accel_Raw"]
            signal = data.loc[beg:end,FOI]
            filt = scipy.signal.butter(3, [1,20], output='sos', btype='bandpass', fs=fs)
            signal_filtered = scipy.signal.sosfilt(filt, signal)
            
            if raw_plot_accel:
                if device == 'Anchored':
                    raw_accel_all_anchored += signal_filtered[:,0]
                elif device == 'Unanchored':
                    raw_accel_all_unanchored += signal_filtered[:,0]
                    
            (f, S) = scipy.signal.periodogram(signal_filtered.T, fs, scaling='density')
            S_l1norm = np.sum(np.abs(S),axis=0)

            if raw_plot_norm:
                plt.semilogy(f, S_l1norm)
                plt.ylim([1e-5, 1e4])
                plt.xlim([0, 100])
                plt.xlabel('frequency [Hz]')
                plt.ylabel('PSD [V**2/Hz]')
                plt.title("Sub {} Condition {} Trial {}".format(sub, device, trial))
                plt.show()
                plt.clf()
            
            peak_freq = f[np.argmax(S_l1norm)]
            peak_amp = S_l1norm[np.argmax(S_l1norm)] #peak amplitude at the peak frequency
            steadiness_dict["Subject"].append(sub)
            steadiness_dict["Trial"].append(trial)
            steadiness_dict["AvgXaccel_True"].append(np.mean(data.loc[beg:end,"X_Accel_True"]))
            steadiness_dict["AvgYaccel_True"].append(np.mean(data.loc[beg:end,"Y_Accel_True"]))
            steadiness_dict["AvgZaccel_True"].append(np.mean(data.loc[beg:end,"Z_Accel_True"]))
            steadiness_dict["peak_freq"].append(peak_freq)
            steadiness_dict["peak_amp"].append(peak_amp)
            steadiness_dict["Device"].append(device)
        except:
            print("Skipping subject {} trial {}...".format(sub,trial))
            
df = pd.DataFrame(steadiness_dict)

if raw_plot_accel:
    numsamples = len(subjects) * 10
    plt.plot(raw_accel_all_anchored/numsamples,'orange')
    plt.plot(raw_accel_all_unanchored/numsamples, 'blue')
    plt.legend(["Anchored X accel","Unanchored X accel"])
    plt.xlabel("Samples")
    plt.ylabel("X Acceleration")
    if is_save:
        plt.savefig(os.path.join(save_path, "filtered_xaccel.svg"))
        plt.savefig(os.path.join(save_path, "filtered_xaccel.png"))
    plt.show()
    plt.clf()

sns.boxplot(data=df, x="Device", y="peak_freq", order=["Unanchored","Anchored"])
sns.stripplot(data=df, x="Device", y="peak_freq",order=["Unanchored","Anchored"],edgecolor="black",linewidth=2)
plt.ylim([0,25])
if is_save:
    plt.savefig(os.path.join(save_path, "steadiness_peakfreq_boxplot.svg"))
    plt.savefig(os.path.join(save_path, "steadiness_peakfreq_boxplot.png"))
plt.show()
plt.clf()

sns.boxplot(data=df, x="Device", y="peak_amp",order=["Unanchored","Anchored"])
sns.stripplot(data=df, x="Device", y="peak_amp", order=["Unanchored","Anchored"], edgecolor="black",linewidth=2)
if is_save:
    plt.savefig(os.path.join(save_path, "steadiness_peakamp_boxplot.svg"))
    plt.savefig(os.path.join(save_path, "steadiness_peakamp_boxplot.png"))
plt.show()
plt.clf()

df_anchored = df[df["Device"] == "Anchored"]
df_unanchored = df[df["Device"] == "Unanchored"]

#stats of peak_freq
pfanchored = df_anchored.loc[:,"peak_freq"]
pfunanchored = df_unanchored.loc[:,"peak_freq"]
res_freq = scipy.stats.ttest_rel(pfanchored,pfunanchored, nan_policy='propagate', alternative='two-sided')
print("*"*10)
print("Pvalue between anchored and unanchored = {}".format(res_freq[1]))
print("Peak Frequency Anchored")
print("mean = {}".format(pfanchored.mean()))
print("median = {}".format(pfanchored.median()))
print("STD = {}".format(pfanchored.std()))
print("SEM = {}".format(pfanchored.std()/np.sqrt(len(pfanchored))))

print("Peak Frequency Unanchored")
print("mean = {}".format(pfunanchored.mean()))
print("median = {}".format(pfunanchored.median()))
print("STD = {}".format(pfunanchored.std()))
print("SEM = {}".format(pfunanchored.std()/np.sqrt(len(pfunanchored))))

#stats of peak_amp
paanchored = df_anchored.loc[:,"peak_amp"]
paunanchored = df_unanchored.loc[:,"peak_amp"]
res_amp = scipy.stats.ttest_rel(paanchored ,paunanchored, nan_policy='propagate', alternative='two-sided')
print("*"*10)
print("Pvalue between anchored and unanchored = {}".format(res_amp[1]))
print("Peak Amplitude Anchored")
print("mean = {}".format(paanchored.mean()))
print("median = {}".format(paanchored.median()))
print("STD = {}".format(paanchored.std()))
print("SEM = {}".format(paanchored.std()/np.sqrt(len(paanchored))))

print("Peak Amplitude Unanchored")
print("mean = {}".format(paunanchored.mean()))
print("median = {}".format(paunanchored.median()))
print("STD = {}".format(paunanchored.std())) 
print("SEM = {}".format(paunanchored.std()/np.sqrt(len(paunanchored))))   

print("exited script with no errors")