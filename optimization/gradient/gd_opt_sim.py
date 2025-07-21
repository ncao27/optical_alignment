from quadoa import *
import numpy as np
from matplotlib import pyplot as plt
import time
import itertools
import math

"""
1. Initialize everything and define all of the parameters

2. Do a random initialization of all the mirror angles within a specific range (the range that I have been simulating)

3. do the gradient based optimization
"""

# allocate a Quadoa core Object
core: QuadoaCore = QuadoaCore()

# select the base folder for where Quadoa is
QuadoaBaseFolder = "E:/Program Files/Quadoa"

# load the available materials
core.loadMaterialFile("E:/Program Files/Quadoa/glass/CDGM.glas")

# load the lens file
ModelFolder = "C:/Users/Nathan Cao/OneDrive/Desktop/quadoa_projects"
core.loadModelFile(ModelFolder + "/beam_walking.optx")

core.applyChangesAndInitModel()


def set_angle(yaw1_angle, yaw2_angle, pitch1_angle, pitch2_angle):
    """
    Parameters
    Functionality
    Returns
    """
    core.setOpticalSystemParamByIndexD(6, 10, yaw1_angle)
    core.setOpticalSystemParamByIndexD(9, 10, yaw2_angle)
    core.setOpticalSystemParamByIndexD(6, 11, pitch1_angle)
    core.setOpticalSystemParamByIndexD(9, 11, pitch2_angle)

def calculate_power():

    data = core.getGeoPSF(0, 0, 0, 17)
    npdata = np.array(data, copy=False)
    nppower = np.sum(npdata)

    return nppower

def global_search(yaws, pitches):
    """
    Parameters
    Functionality
    Returns
    """
    yaw1_start = yaws[0]
    yaw1_end = yaws[1]
    yaw2_start = yaws[2]
    yaw2_end = yaws[3]
    pitch1_start = pitches[0]
    pitch1_end = pitches[1]
    pitch2_start = pitches[2]
    pitch2_end = pitches[3]
    largest_power = 0
    optimal_angle = None

    for yaw1 in range(yaw1_start, yaw1_end, 2):
        for yaw2 in range(yaw2_start, yaw2_end, 2):
            for pitch1 in range(pitch1_start, pitch1_end, 2):
                for pitch2 in range(pitch2_start, pitch2_end, 2):
                    set_angle(yaw1, yaw2, pitch1, pitch2)
                    if calculate_power() >= largest_power:
                        largest_power = calculate_power()
                        optimal_angle = yaw1, yaw2, pitch1, pitch2
    return optimal_angle, largest_power

def perturb(angles, delta):

    # because in the perturb method, we are looking at all four directions, but we dont actually know what current_power
    # is, so while largest_power might be the largest of all four choices, it might not be the largest power overall

    # we set the optimal_angles to None because we can guarantee that an optimal_angles will be set to an angle
    largest_power = -np.inf
    best_direction = np.zeros(4)

    for num_angle in range(1, 5):
        for indices in itertools.combinations(range(4), num_angle):
            for signs in itertools.product([-1, 1], repeat = num_angle):
                direction = np.zeros(4)
                new_angle = np.array(angles, dtype=float)
                for idx, sign in zip(indices, signs):
                    direction[idx] = sign * delta
                    new_angle[idx] += sign * delta

                set_angle(new_angle[0], new_angle[1], new_angle[2], new_angle[3])

                if calculate_power() >= largest_power:
                    largest_power = calculate_power()
                    best_direction = direction

    return largest_power, best_direction

def random_restart():
    yaw1 = np.random.uniform(43, 47)
    yaw2 = np.random.uniform(133, 137)
    pitch1 = np.random.uniform(0, 4) - 2
    pitch2 = np.random.uniform(0, 4) - 2

    return yaw1, yaw2, pitch1, pitch2

def softplus(argument):
    return math.log(1 + math.exp(argument)) - math.log(2)



def grad_optimization(yaws, pitches, iters, delta, momentum, adaptation, epsilon, power_threshold):
    """
    Parameters
        yaws: gives the range of angles the two yaw axes of the mirrors can take on
        pitches: gives the range of angles the two pitch axes of the mirrors can take on
        alpha: the step size to be multiplied by the gradient
        power_threshold: the threshold that must be met for the while loop to stop
        iters: an interation cutoff so overflow does not happen with while loop
        delta: the amount of perturbation to be added to some angle
    Functionality
        This is the gradient-based optimizer that will search for the optimal mirror angles using
        finite difference approximation.
    Returns
        The dictionary of stored values, the number of iter
    """
    start_time = time.time()  # Record start time

    intensities = {}
    current_iter = 1
    learning_rate = delta

    # we first do a global search to get a rough sense of where the most optimal angle might be
    set_angle(yaws[0], yaws[1], pitches[0], pitches[1])
    initial_angle = yaws[0], yaws[1], pitches[0], pitches[1]
    initial_power = calculate_power()

    # set the initial value of intensities to be the angle and power detected by global search
    intensities[initial_angle] = initial_power
    avg_power = initial_power

    velocity = np.zeros(4)

    # start the gradient-based iterations
    while current_iter < iters:

        # if we've hit two of the same values, this must mean that we've hit a max
        if len(list(intensities.keys())) > 1 and int(list(intensities.values())[-1]) != 0 and int(list(intensities.values())[-2]) == int(list(intensities.values())[-1]):
            break

        if np.linalg.norm(list(intensities.keys())[-3:]) < 1e-6:
            angles = random_restart()
            set_angle(angles[0], angles[1], angles[0], angles[1])
            new_power = calculate_power()
            avg_power = new_power
            velocity = np.zeros(4)
            intensities[angles] = new_power

        # get the latest recorded angle
        current_angle = list(intensities.keys())[-1]
        current_power = intensities[current_angle]
        avg_power = 0.8 * avg_power + 0.2 * current_power

        set_angle(current_angle[0], current_angle[1], current_angle[2], current_angle[3])
        if calculate_power() > power_threshold:
            print("basically reached global max")
            break

        if len(list(intensities.keys())) > 1:
            previous_power = list(intensities.values())[-2]
            learning_rate = learning_rate * math.exp(adaptation * (current_power - avg_power) / (current_power + epsilon))

        # perturb the angle and get the new angle and power
        updated_power, updated_direction = perturb(current_angle, delta)
        velocity = momentum * velocity + learning_rate * (updated_direction / delta)
        updated_angle = current_angle + velocity


        # update the intensities dictionary
        intensities[tuple(updated_angle)] = updated_power

        # increase the count of the current iteration
        current_iter += 1

        print("updated angle: " + str(updated_angle) + "updated power: " + str(updated_power) + "elapsed time: " + "bruh")

    end_time = time.time()  # Record end time

    elapsed_time = end_time - start_time  # Calculate elapsed time


    return intensities, current_iter, elapsed_time

