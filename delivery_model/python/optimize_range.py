#author: ben lahner

import scipy.optimize as sco
import math
from calculate_range import ext_min, ext_max

def check_inputs(args):
    #checks for valid inputs. Returns None
    if args.p<=0:
        raise ValueError("p must be greater than 0")
    if args.bound_z[0]<=0 or args.bound_z[1]<=0:
        raise ValueError("z bounds must both be greater than 0")
    if args.bound_z[0] > args.bound_z[1]:
        raise ValueError("z max bound must be greater than z min bound")
    if args.bound_x[0]<=0 or args.bound_x[1]<=0:
        raise ValueError("x bounds must both be greater than 0")
    if args.bound_x[0] > args.bound_x[1]:
        raise ValueError("x max bound must be greater than x min bound")
    if args.min_angle<=0:
        raise ValueError("min_angle must be greater than 0")
    if args.min_angle >= math.pi/2:
        raise ValueError("min_angle must be less than 90 degrees (pi/2)")

def calc_ext_range(weights, p, range_cutoff, degrees=False):
    #weights is [z, x]
    #calculates the acceptable range for eyedrop administration within 0 to range_cutoff
    range_min = ext_min(weights[0], weights[1], p)
    range_max = ext_max(weights[0], weights[1], p) 
    if range_max > range_cutoff: #range of neck extension angles that can successfully deliver a drop to the eye
        ext_range = range_cutoff - range_min
    else:
        ext_range = range_max - range_min
    
    if degrees:
        return -math.degrees(ext_range) #return negative because we want to minimize this value
    else:
        return -ext_range #return negative because we want to minimize this value

def optimize_ext_range(p, range_cutoff, bounds, min_angle):
    initial_guess = [0.1, 0.1]
    args = (p, range_cutoff)
    constraints = [{'type': 'ineq', 'fun': lambda x: -ext_min(x[0], x[1], p) + min_angle}] 
    options = {"maxiter": 100, "disp": False}
    return sco.minimize(calc_ext_range,
                        initial_guess,
                        args,
                        method='SLSQP',
                        bounds=bounds,
                        constraints=constraints,
                        options=options) 

if __name__ == "__main__":
    """
    Finds the optimal values for variables "x" and "z" to maximize the range 
    of acceptable neck extension angles (below the user-defined max neck 
    extension allowed). The result also obeys a user-defined minimum angle
    that the first acceptable neck extension angle needs to be under.
    """
    class arguments():
        def __init__(self):
            #make sure your use of degrees and radians is consistent
            self.p = 10 #palpebral fissure vertical height (PFH) in mm. Typical range is 8-11mm
            self.max_neck_ext = math.radians(35) #maximum neck extension angle allowed in degrees. Set to 35 degrees from literature
            self.bound_z = (1,math.inf) #(min, max) bounds on z (above eye center, mm)
            self.bound_x = (5, math.inf) #(min, max) bounds on x (away from eye, mm)
            self.min_angle = math.radians(20) #a constraint for the minimum neck extension to be smaller than this angle 
    args = arguments()
    
    #check valid inputs
    check_inputs(args)
    
    res = optimize_ext_range(args.p, args.max_neck_ext, (args.bound_z, args.bound_x), args.min_angle)
    print(res)
    if res['success']:
        print("Successfully optimized the function")
        opt_z = res['x'][0]
        opt_x = res['x'][1]
        print(f"Optimal value z (mm): {opt_z}")
        print(f"Optimal value x (mm): {opt_x}")
        theta_min=ext_min(opt_z, opt_x, args.p, degrees=True)
        theta_max=ext_max(opt_z, opt_x, args.p, degrees=True)
        print(f"minimum neck extension (degrees): {theta_min}")
        print(f"maximum neck extension (degrees): {theta_max}")
        print(f"Neck extension range (degrees): {theta_max-theta_min}")
    else:
        print("WARNING: No optimal solution found")


