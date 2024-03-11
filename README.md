# precise-eyedrop
This repository contains code and data to reproduce the numerical results and original plots in the manuscript:

*George-Akpenyi, J., *Lahner, B., *Shim SH., *Smith, C., Singh, N., Murphy, M., Sibanda, L., Traverso G., and Hanumara N.
A mechanical device for precise self-administration of ocular drugs.
Human Factors in Healthcare, 2024.
In revision.

\* denotes equal first authorship
## Project folder structure
See the description of the folder contents after the "#" in the directory tree below.
```
/path/to/your/project
.
├── LICENSE
├── README.md
├── delivery_model #code to calculate and optimize bottle tip position and/or neck extension 
│   ├── matlab
│   └── python
├── exp1_anchoring #code and data pertaining to results "Experiment 1" 
│   ├── anchoring.py
│   ├── data
│   └── output
├── exp2_feedback #code and data pertaining to results "Experiment 2"
│   ├── data
│   ├── feedback.py
│   └── output
├── exp3_placement #code and data pertaining to results "Experiment 3"
│   ├── data
│   ├── output
│   └── placement.py
├── exp4_hitormiss #code and data pertaining to results "Experiment 4"
│   ├── data
│   ├── hitormiss.py
│   └── output
└── images #teaser image for this repository
    └── eyedrop_github_teaser.jpg
```
## Eyedrop delivery model

This Matlab and Python code parameterizes eyedrop delivery based on the human's palpebral fissure height ($P$) (distance beetween upper and lower eyelid), the human's head tilt ($\theta_{tilt}$), the eyedrop bottle tip's distance away from the eye ($X$), and the eyedrop bottle tip's distance above the center of the eye ($Z$), where $X>0$; $P>0$; $Z>-P/2$; $0<=\theta_{tilt}<=\pi/2$. The model assumes a non-curved, 2D eye.

Both the Matlab and Python code implement this eyedrop model. The Matlab code additionally generates a plot of valid head tilts for chosen parameters. The Python code can additionally optimize parameters under specified constraints and bounds.

This eyedrop delivery model was used to design a eyedrop assist device detailed in this publication: [coming soon](link)

If you use this eyedrop delivery model or code, please cite: [coming soon]

![eyedrop model](/images/eyedrop_github_teaser.jpg)

## Derivation of eyedrop delivery model formulas

At neutral head tilt (tilt=0), we define the radius ($r$) and angle ($\theta$) for points $P_b$ and $P_t$ and $D$:

$r_{Pb}=0$

$r_{Pt}=P$

$r_D=X^2+(Z+P/2)^2$

$P_b=0$

$P_t=\pi/2$

$D=arctan((Z+P/2)/X)$

The x-axis location ($L$) of each point is then given by:

$L_{Pb}=r_{Pb}*cos(P_b+\theta_{tilt})$

$L_{Pt}=r_{Pt}*cos(P_t+\theta_{tilt})$

$L_D=r_D*cos(D+\theta_{tilt})$

The minimum head tilt ($\theta_{min}$) for a successful drop occurs when the location along the x-axis of the bottle tip ($D$) equals that of the bottom eyelid ($P_b$):

$L_D=L_{Pb}$

$r_D*cos(D+\theta_{min})=r_{Pb}*cos(P_b+\theta_{min})$

$r_D*cos(D+\theta_{min})=0$

Ignoring the trivial solution of $r_D=0$, we get:

$cos(D+\theta_{min})=0$

$D+\theta_{min}=\pi/2$

$\theta_{min}=\pi/2-D$

$\theta_{min}=\pi/2-arctan((Z+P/2)/X)$

Similarly, the maximum head tilt ($\theta_{max}$) for a successful drop occurs when the location along the x-axis of the bottle tip ($D$) equals that of the upper eyelid ($P_t$):

$L_D=L_{Pt}$

$r_D*cos(D+\theta_{max})=r_{Pt}*cos(P_t+\theta_{max})$

$\theta_{max}$ can be solved for using this above equation, or, more simply, one can graphically see in Figure panel C:

$\theta_{max}=\pi/2$ for $Z<=P/2$ and

$\theta_{max}=\pi/2-arctan((Z-P/2)/X)$ for $Z>P/2$

Lastly, the range of head tilts for a successful eyedrop delivery occurs at head tilts in between the minimum and maximum head tilts:

$\theta_{range}=\theta_{max}-\theta_{min}$
