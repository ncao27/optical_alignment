####################################################
#       Quadoa Optical CAD - Python Modul          #
#  FFT PSF Diagram for all Fields and Wavelengths  #
####################################################
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
ModelFolder = "C:/Users/Nathan Cao/OneDrive/Desktop/quadoa projects"
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

yaw1_start = 43; yaw1_end = 47; yaw2_start = 133; yaw2_end = 137
pitch1_start = -2; pitch1_end = 2; pitch2_start = -2; pitch2_end = 2
step_size = 0.2; size = (yaw1_end - yaw1_start) / step_size
intensities = np.ones((int(size) + 1, int(size) + 1, int(size) + 1, int(size) + 1))

'''
core.setOpticalSystemParamByIndexD(6, 10, 44)
core.setOpticalSystemParamByIndexD(9, 10, 135)
data = core.getFFTPSF(0, 0, 0, 100, 100)
npdata = np.array(data, copy=False)
nppower = np.sum(npdata)
print(nppower)
'''


# 4 degrees of freedom case
yaw1 = yaw1_start; yaw2 = yaw2_start; pitch1 = pitch1_start; pitch2 = pitch2_start
index1 = 0; index2 = 0; index3 = 0; index4 = 0

while yaw1 < yaw1_end:

    # update the yaw of the first mirror
    core.setOpticalSystemParamByIndexD(6, 10, yaw1)

    yaw2 = yaw2_start

    while yaw2 < yaw2_end:

        core.setOpticalSystemParamByIndexD(9, 10, yaw2)

        pitch1 = pitch1_start

        while pitch1 < pitch1_end:

            core.setOpticalSystemParamByIndexD(6, 11, pitch1)

            pitch2 = pitch2_start

            while pitch2 < pitch2_end:

                # update the yaw of the second mirror
                core.setOpticalSystemParamByIndexD(9, 11, pitch2)

                # getGeoPSF, as opposed to get FFT
                data = core.getGeoPSF(0, 0, 0, 100)

                # this is just the numpy array version of the PSF
                npdata = np.array(data, copy=False)

                # compute the total power of the psf (because it's discrete we just use the sum function
                nppower = np.sum(npdata)

                # store the intensity values in our matrix
                intensities[index1, index2, index3, index4] = nppower

                index4 += 1
                pitch2 += step_size
                print("Pitch2: " + str(pitch2) + " Pitch1: " + str(pitch1) + " Yaw2: " + str(yaw2) + " Yaw1: " + str(yaw1))
            index3 += 1
            pitch1 += step_size
            index4 = 0

        index2 += 1
        yaw2 += step_size
        index3 = 0

    index1 += 1
    yaw1 += step_size
    index2 = 0

    print(str(yaw1))

# normalize the intensity values because too big
intensities_normalized = intensities / np.max(intensities)
#save_path = r"C://Users//Nathan Cao//Desktop//quadoa projects//intensities_geo_0_2_fourdeg.npy"
np.save('intensities_geo_0_2_fourdeg2.npy', intensities_normalized)



#2 degrees of freedom case
'''
while yaw1 < yaw1_end:

    # update the yaw of the first mirror
    core.setOpticalSystemParamByIndexD(6, 10, yaw1)

    yaw2 = yaw2_start

    while yaw2 < yaw2_end:

        # update the yaw of the second mirror
        core.setOpticalSystemParamByIndexD(9, 10, yaw2)

        # getGeoPSF, as opposed to get FFT
        data = core.getGeoPSF(0, 0, 0, 100)

        # this is just the numpy array version of the PSF
        npdata = np.array(data, copy=False)

        # compute the total power of the psf (because it's discrete we just use the sum function
        nppower = np.sum(npdata)

        # store the intensity values in our matrix
        intensities[index1, index2] = nppower

        index2 += 1
        yaw2 += step_size
        print(str(yaw2))

    index1 += 1
    yaw1 += step_size
    index2 = 0

    print(str(yaw1))
'''