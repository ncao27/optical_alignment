####################################################
#       Quadoa Optical CAD - Python Modul          #
#  FFT PSF Diagram for all Fields and Wavelengths  #
####################################################
from quadoa import *
import numpy as np
from matplotlib import pyplot as plt
from joblib import Parallel, delayed
import csv

'''
# Get info about the sequence: the sequence number, the number of fields, wavelengths, etc.
seq_nr = 0
max_field = core.getNrFields(seq_nr)
max_wave = core.getNrWavelengths(seq_nr)
surf = core.getSequenceImageSurface(seq_nr)

# Set all of the parameter values and the initial values
fig, axs = plt.subplots(max_wave, max_field, squeeze=False)
'''

# Set the necessary parameter values
yaw1_start = 43; yaw1_end = 47; yaw2_start = 133; yaw2_end = 137
pitch1_start = -2; pitch1_end = 2; pitch2_start = -2; pitch2_end = 2; step_size = 1

# Generate the values that we are going to use
yaw1s = np.arange(yaw1_start, yaw1_end, step_size)
yaw2s = np.arange(yaw2_start, yaw2_end, step_size)
pitch1s = np.arange(pitch1_start, pitch1_end, step_size)
pitch2s = np.arange(pitch2_start, pitch2_end, step_size)

# Function defining the simulation
def run_simulation(yaw1, yaw2, pitch1, pitch2):
    # Define paths and set up a quadoa core
    core: QuadoaCore = QuadoaCore()

    QuadoaBaseFolder = "E:/Program Files/Quadoa"
    # load material catalogs
    core.loadMaterialFile("E:/Program Files/Quadoa/glass/CDGM.glas")

    # load the lens file
    ModelFolder = "C:/Users/Nathan Cao/OneDrive/Desktop/quadoa_projects"
    core.loadModelFile(ModelFolder + "/beam_walking.optx")

    core.applyChangesAndInitModel()

    # set the pitch and yaw values
    core.setOpticalSystemParamByIndexD(6, 10, yaw1)
    core.setOpticalSystemParamByIndexD(9, 10, yaw2)
    core.setOpticalSystemParamByIndexD(6, 11, pitch1)
    core.setOpticalSystemParamByIndexD(9, 11, pitch2)

    # getGeoPSF, as opposed to get FFT
    data = core.getGeoPSF(0, 0, 0, 100)

    # this is just the numpy array version of the PSF
    npdata = np.array(data, copy=False)

    # compute the total power of the psf (because it's discrete we just use the sum function
    nppower = np.sum(npdata)

    return yaw1, yaw2, pitch1, pitch2, nppower

# Do the parallel computation of the simulations
Results = Parallel(n_jobs=-1, verbose=100)(
    delayed(run_simulation)(i, j, k, l)
    for i in yaw1s for j in yaw2s for k in pitch1s for l in pitch2s
)

# Define the parameters for how we want to set the filename and filepath
simulation_num = 2
filename = "geometric_fourdeg_" + str(simulation_num) + ".csv"
filepath = "C://Users//Nathan Cao//OneDrive//Desktop//quadoa_projects//intensity_data//four_deg//"
cleaned_results = [tuple(row) if hasattr(row, '__iter__') and not isinstance(row, str) else (row,) for row in Results]

# Generate the actual csv file
with open(filepath + filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['yaw1', 'yaw2', 'pitch1', 'pitch2', 'intensity'])  # header
    writer.writerows(cleaned_results)
