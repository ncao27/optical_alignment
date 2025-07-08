import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# read in the csv file that we will do analysis with; file with 0.05 fft is the one thats correct
intensities = pd.read_csv("C://Users//Nathan Cao//OneDrive//Desktop//quadoa projects//intensity_data//intensities_geo_0_05.csv")
intensities = intensities.drop(intensities.columns[[80]], axis = 1)

# variables used later
m1_start = 43; m1_end = 47; m2_start = 133; m2_end = 137; step_size = 0.05
size1 = (m1_end - m1_start) / step_size; size2 = (m2_end - m2_start) / step_size

# generate the list of values
yaw1 = np.arange(m1_start, m1_end, step_size)
yaw2 = np.arange(m2_start, m2_end, step_size)
Y1, Y2 = np.meshgrid(yaw1, yaw2)

fig = plt.figure(figsize = (10, 8))
ax = fig.add_subplot(111, projection='3d')

# plotting the surface, we can use "rstride" and "cstride" to control the densities
surf = ax.plot_surface(
    Y1, Y2, intensities,
    cmap = 'viridis',
    edgecolor = 'none',
    rstride = 1,
    cstride = 1
)

# set all of the labels and the title
ax.set_xlabel('Mirror 1 Yaw Angle (deg)')
ax.set_ylabel('Mirror 2 Yaw Angle (deg)')
ax.set_zlabel('Intensity')
ax.set_title('PSF Intensity vs. Mirror Angles')

# add the color bar
fig.colorbar(surf, ax=ax, shrink=0.5, label='Intensity')

# show the plot
plt.tight_layout()
plt.show()

# Plot the 2D intensity map
im = plt.imshow(intensities,
                extent=(Y2.min(), Y2.max(), Y1.min(), Y1.max()),
                cmap='viridis',
                aspect='auto',
                origin='lower')

# Add labels and title
plt.xlabel('Mirror 2 Yaw Angle (deg)')
plt.ylabel('Mirror 1 Yaw Angle (deg)')
plt.title('PSF Intensity vs. Mirror Angles')

# Add colorbar
cbar = plt.colorbar(im)
cbar.set_label('Intensity')

# Show the plot
plt.tight_layout()
plt.show()


