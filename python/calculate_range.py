#author: ben lahner

import math
import numpy as np
from scipy.optimize import minimize

def ext_min(z, x, p, degrees=False):
    #minimum neck extension angle required for successful drop
    #If degrees is False (default), result is returned in radians
    angle = math.pi/2 - math.atan2(z+p/2, x) #theta_d
    if degrees:
        return math.degrees(angle)
    else:
        return angle

def ext_max(z, x, p, degrees=False):
    #maximum neck extension possible for successful drop
    #If degrees is False (default), result is returned in radians
    def func(X, z, x, p): # r_d, theta_d, r_pt, theta_pt):
        return [np.abs(np.sqrt(x**2 + (z+p/2)**2)*np.cos(math.atan2(z+p/2, x)+ X[0]) - p*np.cos(math.pi/2 + X[0]))]
    #minimizing the equation allows us to specify bounds
    r = minimize(func,
                 [0], 
                 args=(z,x,p),
                 method="SLSQP",
                 bounds=[(0,math.pi/2)],
                 )
    angle = r['x'][0]
    if angle == 0:
        angle = math.pi/2 #change angle to pi/2 radians if angle that minimizes equation is 0
    if degrees:
        return math.degrees(angle)
    else:
        return angle

if __name__ == '__main__':
    """
    Given x, z, and p, what is the head tilt range for a successful drop delivery?
    """
    class arguments():
        def __init__(self):
            self.p = 10 #palpebral fissure height (distance between upper and lower eyelid), in mm
            self.z = 12 #distance above the center of the eye, in mm
            self.x = 5 #distance away from the center of the eye, in mm
    args = arguments()
    
    if args.p<=0:
        raise ValueError("p must be greater than 0")
    if args.z<=-args.p/2:
        raise ValueError("z must be greater than -p/2")
    if args.x<=0:
        raise ValueError("x must be greater than 0")
    
    #search_max(args.z, args.x, args.p, degrees=True)
    theta_min = ext_min(args.z, args.x, args.p, degrees=True)
    theta_max = ext_max(args.z, args.x, args.p, degrees=True)
    print("For parameters:")
    print(f"palpebral fissure heigth (p, mm) = {args.p}")
    print(f"distance above center of eye (Z, mm) = {args.z}")
    print(f"distance away from eye (x, mm) = {args.x}")
    print(f"Head tilt range for successful eye drop delivery is {theta_min} --> {theta_max}")