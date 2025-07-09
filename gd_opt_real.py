from PowermeterSample import get_power_value
import subprocess
import random
import numpy as np

# define the file path of the python script that interfaces with the motors
motor_interface = "C://Users//Nathan Cao//OneDrive//Desktop//motor_interface//hyperterminal.py"

def set_adjust(direction, frequency, steps, axes):
    """
    Params:
        1. 
    """
    for axis in axes:
        inputs = [
            direction,
            str(frequency),
            str(steps),
            axis
        ]
        input_data = "\n".join(inputs) + "\n"

        # call the script and send input
        process = subprocess.run(
            ["python", motor_interface],
            input=input_data,
            text=True,
            capture_output=True
        )
def random_params():
    options = ["NR", "RR"]
    direction = random.choice(options)
    steps = np.random.randint(2000, 5000)
    return direction, steps


def optimize_power(iters, target_power):
    """
    Policy: if after iters number of iterations we do not get target_power then we exit out, target_power should be above 0.5mW
    """
    # if it is less than 100 micro watts, then it must be the case that the power meter is directed towards nothing, we must do a random restart

    power_dir = {}
    frequency = 1000
    counter = 0

    while get_power_value() <= 1e-4 and counter < iters:

        if get_power_value() >= target_power:
            break

        # Create a list containing the two strings
        direction = random_params()[0]
        steps = random_params()[1]
        axes = ["A", "C"]

        set_adjust(direction, frequency, steps, axes)

        counter += 1
        power_dir[get_power_value()] = (direction, str(frequency), str(steps))
        print(get_power_value())

    while get_power_value() > 1e-4 and counter < iters:

        # if we reach target power value we exit the system
        if get_power_value() >= target_power:
            break

        # only if we have two datapoints, then we can do finite difference approximation
        if len(power_dir.keys()) > 1:
            # if the last key has a power reading greater than the previous one, we work in that direction
            last_key = list(power_dir.keys())[-1]
            second_last_key = list(power_dir.keys())[-2]

            if last_key > second_last_key:

                # calculating the number of steps that we should use
                power_diff = last_key - second_last_key
                tolerance = 1e-10
                sensitivity = 1e-4
                normalized = 1 / (1 + (power_diff / sensitivity) + tolerance)
                min_step = 1000
                max_step = 5000

                # setting the values for the experiment
                direction = power_dir[last_key][0]
                steps = min_step + (max_step - min_step) * normalized
                axes = ["A", "C"]

                set_adjust(direction, frequency, steps, axes)

            # if the values are the same we pick another random direction to go
            elif last_key == second_last_key or last_key - second_last_key < 2e-6:
                direction = random_params()[0]
                steps = random_params()[1]
                axes = ["A", "C"]

                set_adjust(direction, frequency, steps, axes)

            # if the value dropped, we take exact same values and return to the original spot
            else:
                if power_dir[last_key][0] == "NR":
                    direction = "RR"
                direction = "NR"
                frequency = power_dir[last_key][1]
                steps = power_dir[last_key][2]
                axes = ["A", "C"]

                set_adjust(direction, frequency, steps, axes)


        # if we don't have more than two readings, we pick a random direction to go
        if len(power_dir.keys()) <= 1:

            direction = random_params()[0]
            steps = random_params()[1]
            axes = ["A", "C"]

            set_adjust(direction, frequency, steps, axes)

            counter += 1
            power_dir[get_power_value()] = (direction, str(frequency), str(steps))

        print(get_power_value())
        counter += 1

    return counter



optimize_power(2000, 0.7)













