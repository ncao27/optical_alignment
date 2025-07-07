import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import math
import seaborn as sns
import plotly.express as px

# read in the csv file that we will do analysis with; file with 0.05 fft is the one thats correct
experiment_num = 1
filepath = "C://Users//Nathan Cao//OneDrive//Desktop//quadoa_projects//intensity_data//four_deg//experiment_" + str(experiment_num)

# find all of the csv files using the path that we defined
csv_files = sorted(glob.glob(filepath + "//*.csv"))  # e.g., "*.csv"

# load the csv files and concatenate all of them
df_list = [pd.read_csv(f) for f in csv_files]
intensities = pd.concat(df_list, ignore_index=True)
intensities = intensities.round(1)