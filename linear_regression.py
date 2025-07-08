import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D
import glob

# read in the csv file that we will do analysis with; file with 0.05 fft is the one thats correct
experiment_num = 1
filepath = "C://Users//Nathan Cao//OneDrive//Desktop//quadoa_projects//intensity_data//four_deg//experiment_" + str(experiment_num)

# find all of the csv files using the path that we defined
csv_files = sorted(glob.glob(filepath + "//*.csv"))  # e.g., "*.csv"

# load the csv files and concatenate all of them
df_list = [pd.read_csv(f) for f in csv_files]
intensities = pd.concat(df_list, ignore_index=True)
intensities = intensities.round(1)
np_data = intensities.to_numpy()
np_data = np_data / np.max(np_data)

angular_data = np_data[:, :4]
intensity_data = np_data[:, 4]

model = LinearRegression()
model.fit(angular_data, intensity_data)

'''
We first pick an angular step size in degrees. We take the gradient which is model.coef_ of the line of best fit 
(confusion: why is the gradient not changing as we update the angular values?). We keep updating the parameters until it 
converges?
'''

angular_step = 0.005


print(model.coef_)