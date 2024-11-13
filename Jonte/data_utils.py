import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plt_nans(df):
	nan_counts = df.isna().sum()
	nan_counts = nan_counts[nan_counts > 0]
	sns.barplot(x=nan_counts.index, y=nan_counts.values, hue=nan_counts.index, palette=my_palette(len(nan_counts.index)), alpha=0.7)
	plt.show()

def type_mask(df):
	mask = pd.DataFrame()
	for col in df.columns:
		nans = df[df[col].isna()][col]
		other = df[df[col].notna()][col]
		other = other.apply(lambda x: type(x))
		nans = nans.apply(lambda x: np.nan)
		mask[col] = pd.concat([other, nans])
	return mask

def uniques(df):
	for col in df.columns:
		print(f"{col} : {df[col].unique()}")

def my_palette(size):
	return sns.color_palette("blend:#00D9FF,#D2FF61", n_colors=size)

def df_to_numeric(df, error="raise"):
	for col in df.columns:
		df[col] = pd.to_numeric(df[col], errors=error)
		return df
	 