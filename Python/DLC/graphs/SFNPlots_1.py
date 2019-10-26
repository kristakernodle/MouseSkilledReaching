#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:54:36 2019

@author: kkrista
"""

import matplotlib.pyplot as plt
import numpy as np

mean_EDLeft_fft =np.mean(mean_EDLeft_fft,axis=1)
mean_EDRight_fft =np.mean(mean_EDRight_fft,axis=1)

mean_ED = np.mean([mean_EDLeft_fft,mean_EDRight_fft],axis=0)

mean_leftPaw_fft =np.mean(mean_leftPaw_fft,axis=1)
mean_rightPaw_fft =np.mean(mean_rightPaw_fft,axis=1)

mean_paws = np.mean([mean_leftPaw_fft,mean_rightPaw_fft],axis=0)

rows = 2
cols = 1

fig, axs = plt.subplots(rows,cols,figsize=(15.3,9.7),dpi=300)

line1a, = axs[0].plot(mean_paws,'b',label='Abnormal Movement')
line1b, = axs[0].plot(mean_paws_grooming,color='#da6d05',label='Grooming Movement')
line1a.set_linewidth(4)
line1b.set_linewidth(4)
axs[0].set_ylim(0,4000)
axs[0].set_xlim(0,20)
axs[0].set_xlabel('Frequency',size=20)
axs[0].set_ylabel('Power',size=20)
axs[0].set_title('Mean Left and Right Paw Spectrogram',size = 36)
axs[0].legend(fontsize=20)

   
line2a, = axs[1].plot(mean_ED,'b')
line2b,=axs[1].plot(mean_ED_grooming,color='#da6d05')
line2a.set_linewidth(4)
line2b.set_linewidth(4)
axs[1].set_ylim(0,4000)
axs[1].set_xlim(0,20)
axs[1].set_xlabel('Frequency',size=20)
axs[1].set_ylabel('Power',size=20)
axs[1].set_title('Mean Euclidean Distance Spectrogram',size = 36)

fig.tight_layout()
fig.subplots_adjust(hspace=0.5)
fig.savefig('/Users/kkrista/Desktop/spectrogram.pdf')

