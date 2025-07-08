from quadoa import *
import numpy as np
from matplotlib import pyplot as plt
import time
from multiprocessing import Pool, cpu_count
# allocate a Quadoa core Object
core: QuadoaCore = QuadoaCore()

QuadoaBaseFolder = "E:/Program Files/Quadoa"
# load material catalogs
core.loadMaterialFile("E:/Program Files/Quadoa/glass/CDGM.glas")

# load the lens file
ModelFolder = "C:/Users/Nathan Cao/OneDrive/Desktop/quadoa_projects"
core.loadModelFile(ModelFolder + "/beam_walking.optx")

core.applyChangesAndInitModel()
print(type(core))

# get basic information about the sequence; we get the maxes for the for loop underneath
seq_nr = 0
max_field = core.getNrFields(seq_nr)
max_wave = core.getNrWavelengths(seq_nr)
surf = core.getSequenceImageSurface(seq_nr)

# we gonna plot the PSFs of the different fields and the individual wavelengths; currently we just have one of each
fig, axs = plt.subplots(max_wave, max_field, squeeze=False)

'''
Here's what we are going to do. This file is dedicated to performing gradient-based optimization which is different
from training a model. We are going to initiate random values for the yaws and the pitches of the different mirrors. 
And then we can incorporate random restarts, so if the power meter reading is 0 we can do a random restart and see the 
power meter reading. 
'''

yaw1_init = np.random.uniform(43, 47)
yaw2_init = np.random.uniform(133, 137)
pitch1_init = np.random.uniform(-2, 2)
pitch2_init = np.random.uniform(-2, 2)

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
    data = core.getGeoPSF(0, 0, 0, 17)

    # this is just the numpy array version of the PSF
    npdata = np.array(data, copy=False)

    # compute the total power of the psf (because it's discrete we just use the sum function
    nppower = np.sum(npdata)

    return yaw1, yaw2, pitch1, pitch2, nppower