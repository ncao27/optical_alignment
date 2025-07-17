from PowermeterSample import get_power_value
import subprocess
import csv
import time

# define the file path of the python script that interfaces with the motors
motor_interface = "C://Users//Nathan Cao//OneDrive//Desktop//motor_interface//hyperterminal.py"

def set_adjust(direction, frequency, steps, axes):
    """
    Function:
        Calls the hyperterminal.py file and rotates the motor by a specified amount
    Params:
        1. direction: the direction (CW or CCW) that we want the axis of the motor to turn
        2. frequency: the rate at which we want the axis of the motor to turn
        3. steps: the number of pulses
        4. axes: specifically which axes we are going to rotate
    Returns:
        Nothing
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

duration = 1 * 60 * 2
start_time = time.time()
power_readings = []
iters = 1
while time.time() - start_time < duration:
    set_adjust("RR", 200, 1000, ["A"])
    time.sleep(0.5)
    iters += 1
    power_readings.append((get_power_value(), iters))
    print(power_readings)


with open("gauss1_axisA_Freq1500steps500.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(power_readings)
