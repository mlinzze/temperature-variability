#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import socket

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator

import seaborn as sns
import geopandas as gpd

VARIABLE_LABELS = {'T_mean': 'annual mean temperature',
					'T_std': 'seasonal temperature variability',
					'T_range': 'seasonal temperature variability',
					'T_bystd': 'interannual temperature variability',
					'T_ds_bystd': 'interannual temperature variability',
					'T_bdstd': 'day-to-day temperature variability',
					'T_ac_bdstd': 'day-to-day temperature variability',
					'T_dt_mean': 'annual mean temperature (dt)',
					'T_dt_std': 'seasonal temperature variability (dt)',
					'T_dt_bystd': 'interannual temperature variability (dt)',
					'log_population_density': 'log Pop. density'}


df_data1 = pd.read_csv('./data/climate_1985-2014.csv')
df_data2 = pd.read_csv('./data/socioeconomic.csv')
df_data = df_data1.merge(df_data2, on=['latitude', 'longitude'], how='outer')

## ============================================================= ##
## four variables in one plot as rows

experiment = 'A03'

fig, axes = plt.subplots(6, sharex=True, gridspec_kw={'hspace': 0.6, 'height_ratios': [4, 4, 4, 4, 1, 1]}, figsize=(8,6))

for v, var in enumerate(['T_mean', 'T_ac_bdstd', 'T_range', 'T_ds_bystd']):

	variable = var
	print(variable)

	# read in results (T_mean)
	df_all = pd.DataFrame()
	datapath = "./results"
	datafile = "coeffs_{0:s}.csv".format(experiment)

	if os.path.exists(os.path.join(datapath, datafile)):
		df = pd.read_csv(os.path.join(datapath, datafile))
	else:
		print('Not found: ', datafile)

	labels = ['T_mean_c41', 'T_mean_c42', 'T_mean_c43', 'T_mean_c44', 'T_mean_c45', 'T_mean_c46', 'T_mean_c47', 'T_mean_c48', 'T_mean_c49']
	for label in labels:
		coeff = df.loc[df.iloc[:, 0].str.contains(label) & df.iloc[:, 0].str.contains(':{0:s}'.format(variable)), 'coef.model_fixest.'].values[0]
		se = df.loc[df.iloc[:, 0].str.contains(label) & df.iloc[:, 0].str.contains(':{0:s}'.format(variable)), 'se'].values[0]
		df_all = df_all.append({'variable': variable, 'labels': label, 'coeff': coeff, 'se': se}, ignore_index=True)

	df_sub = df_all.loc[df_all['variable'] == variable, :]
	x = np.arange(np.size(labels))
	y = df_sub['coeff']
	se = df_sub['se']
	axes[v].annotate(text="Coefficients of " + VARIABLE_LABELS[variable], xy=(0.01, 0.99), xycoords="axes fraction", va="bottom", ha="left")
	axes[v].plot(x, y, 'ko')
	#axes[v].set_xticks(x)
	#axes[v].set_xticklabels(['(, -8)', '[-8, -4)', '[-4, 0)', '[0, 4)', '[4, 8)', '[8, 12)', '[12, 16)', '[16, 20)', '[20, 24)', '[24, 28)', '[28, 32)', '(32, )'])
	axes[v].set_xticks(x[:-1] + 0.5)
	axes[v].set_xticklabels([str(i) for i in range(0, 32, 4)])
	#axes[v].set_xlim([0., 1.])
	axes[v].errorbar(x, y, yerr=1.96*se, fmt='o', capsize=4., elinewidth=2., capthick=2, markersize=2., lw=0.5, color='k')
	axes[v].set_ylabel('Coeff. in bin')
	axes[v].plot(axes[v].get_xlim(), [0., 0.], 'k-', lw=0.5)
	sns.despine(ax=axes[v], offset=5., right=True, top=True)
	axes[v].grid(axis='x')

lims = np.arange(0., 32.+4, 4.)
for i, lim in enumerate(lims):
	if i == 0:
		dfsub = df_data.loc[(df_data['T_mean'] < lim), :]
	elif lim == 28.:
		dfsub = df_data.loc[(df_data['T_mean'] >= lims[i-1]), :]
	else:
		dfsub = df_data.loc[(df_data['T_mean'] >= lims[i-1]) & (df_data['T_mean'] < lim), :]
	y = dfsub['T_mean'].count()
	axes[-2].bar(i, height=y, width=1.0, color='#969696')
axes[-2].yaxis.set_label_position("right")
axes[-2].yaxis.tick_right()
axes[-2].set_ylabel('cells')
axes[-2].set_yticklabels([])
axes[-2].grid(axis='x')
sns.despine(ax=axes[-2], offset=5., left=True, right=False, top=True)

for i, lim in enumerate(lims):
	if i == 0:
		dfsub = df_data.loc[(df_data['T_mean'] < lim), :]
	elif lim == 28.:
		dfsub = df_data.loc[(df_data['T_mean'] >= lims[i-1]), :]
	else:
		dfsub = df_data.loc[(df_data['T_mean'] >= lims[i-1]) & (df_data['T_mean'] < lim), :]
	y = dfsub['POPULATION_2015'].sum()
	axes[-1].bar(i, height=y, width=1.0, color='#969696')
axes[-1].yaxis.tick_right()
axes[-1].yaxis.set_label_position("right")
axes[-1].set_ylabel('popul.')
axes[-1].set_yticklabels([])
axes[-1].grid(axis='x')
sns.despine(ax=axes[-1], offset=5., left=True, right=False, top=True)

axes[-1].set_xlabel('Annual mean temperature (deg C)')

fig.savefig('./figures/coefficients_{0:s}_4C_4rows.pdf'.format(experiment), bbox_inches='tight')
