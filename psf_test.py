####################################################
#       Quadoa Optical CAD - Python Modul          #
#  FFT PSF Diagram for all Fields and Wavelengths  #
####################################################
from quadoa import *
import numpy as np
from matplotlib import pyplot as plt 

# allocate a Quadoa core Object
core: QuadoaCore = QuadoaCore()

QuadoaBaseFolder = "E:/Program Files/Quadoa"
# load material catalogs
core.loadMaterialFile("E:/Program Files/Quadoa/glass/CDGM.glas")

# load the lens file 
ModelFolder = "C:/Users/Nathan Cao/OneDrive/Desktop/quadoa projects"
core.loadModelFile(ModelFolder + "/beam_walking.optx")

core.applyChangesAndInitModel()

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
