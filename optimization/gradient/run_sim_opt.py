import gd_opt_sim as gd_sim
import numpy as np

def initialize_angles():
    yaw1 = np.random.uniform(43, 47)
    yaw2 = np.random.uniform(133, 137)
    pitch1 = np.random.uniform(0, 4) - 2
    pitch2 = np.random.uniform(0, 4) - 2

    return yaw1, yaw2, pitch1, pitch2

start_angle = initialize_angles()
start_yaws = [start_angle[0], start_angle[1]]
start_pitches = [start_angle[2], start_angle[3]]
results = gd_sim.grad_optimization(start_yaws, start_pitches, 1000, 0.02, 0.9, 0.1, 1e-6, 13150000)
print(results)