####################################################
#       Quadoa Optical CAD - Python Modul          #
# Plot Spot Diagram for all Fields and Wavelengths #
####################################################
from quadoa import *
import numpy as np
from matplotlib import pyplot as plt
import time

# allocate a Quadoa core Object
core: QuadoaCore = QuadoaCore()

QuadoaBaseFolder = "E:/Program Files/Quadoa"
# load material catalogs
core.loadMaterialFile("E:/Program Files/Quadoa/glass/CDGM.glas")

# load the lens file 
ModelFolder = "C:/Users/Nathan Cao/OneDrive/Desktop/quadoa projects"
core.loadModelFile(ModelFolder + "/beam_walking.optx")

core.applyChangesAndInitModel()

seq_nr = 0
max_field = core.getNrFields(seq_nr)
max_wave = core.getNrWavelengths(seq_nr)
surf = core.getSequenceImageSurface(seq_nr)

# perform a raytrace
core.traceAllRays()   

# setup plot matrix
fig, axs = plt.subplots(max_wave, max_field, squeeze=False)

for field in range(max_field):
    for wave in range(max_wave):
        spot = core.getRayPos(seq_nr, field, wave, surf)
        axs[wave, field].set_title("Field: " + str(field) + " Wave : " + str(wave))
        npspot = np.array(spot, copy=True)

        axs[wave, field].plot(npspot[0,:], npspot[1,:], ".", markersize=1) #,".", color="r")
        axs[wave, field].set_xlabel("x / mm") 
        axs[wave, field].set_ylabel("y / mm") 
        axs[wave, field].axis('equal')

fig.tight_layout()
plt.show()


# get basic information about the sequence
seq_nr = 0
max_field = core.getNrFields(seq_nr)
max_wave = core.getNrWavelengths(seq_nr)
surf = core.getSequenceImageSurface(seq_nr)

fig, axs = plt.subplots(max_wave, max_field, squeeze=False)

for wave in range(max_wave):
    for field in range(max_field):
        data = core.getFFTPSF(0, field, wave, 100, 100);
        npdata = np.array(data, copy=False)
        axs[wave, field].imshow(npdata)

fig.tight_layout()
plt.show()
