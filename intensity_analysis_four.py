import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import seaborn as sns
import plotly.express as px

# read in the csv file that we will do analysis with; file with 0.05 fft is the one thats correct
experiment_num = 1
filepath = "C://Users//Nathan Cao//OneDrive//Desktop//quadoa_projects//intensity_data//four_deg//experiment_" + str(experiment_num)

# find all of the csv files using the path that we defined
csv_files = sorted(glob.glob(filepath + "//*.csv"))  # e.g., "*.csv"

# load the csv files and concatenate all of them
df_list = [pd.read_csv(f) for f in csv_files]
df_all = pd.concat(df_list, ignore_index=True)

# convert the dataframe to a numpy matrix
intensities = df_all.to_numpy()


# variables that are used later
yaw1_start = 43; yaw1_end = 47; yaw2_start = 133; yaw2_end = 137
pitch1_start = -2; pitch1_end = 2; pitch2_start = -2; pitch2_end = 2
step_size = 0.5; size = (yaw1_end - yaw1_start) / step_size

# generate the list of values
yaw1 = np.arange(yaw1_start, yaw1_end, step_size)
yaw2 = np.arange(yaw2_start, yaw2_end, step_size)
pitch1 = np.arange(pitch1_start, pitch1_end, step_size)
pitch2 = np.arange(pitch2_start, pitch2_end, step_size)

'''
# ask for whether we want to analyze 2d or 3d cross section
dimension = input("Whether to analyze twod or threed: ").strip()

if dimension == "twod":
    x1, x2 = np.meshgrid(yaw1, yaw2)
    print(x1.shape)

    # we look at the yaw so we fix the pitch
    x3 = 0
    x4 = 0

    # start plotting the figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # plotting the surface, we can use "rstride" and "cstride" to control the densities
    surf = ax.plot_surface(
        x1, x2, intensities[x3, x4, :, :],
        cmap='viridis',
        edgecolor='none',
        rstride=1,
        cstride=1
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
    im = plt.imshow(intensities[:, :, x3, x4],
                    extent=(x2.min(), x2.max(), x1.min(), x1.max()),
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

if dimension == "threed":
    # Suppose you want to select data where x4 == 0.5
    x4_value = 0
    
    # Use np.isclose if x4 is a float and might have rounding issues
    subset_df = df_all[np.isclose(df_all['pitch2'], x4_value)]
    
    # Plot using plotly.express
    fig = px.scatter_3d(df_all, x='yaw1', y='yaw2', z='pitch1',
                        color='intensity',
                        color_continuous_scale='Viridis',
                        title='4D Plot: x1, x2, x3 with intensity color')
    
    fig.update_layout(scene=dict(
        xaxis_title='x1',
        yaxis_title='x2',
        zaxis_title='x3'
    ))
    
    fig.show()
'''