#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import copy

import numpy as np
import pandas as pd

import statsmodels
import statsmodels.api as sm

### ==========================================

labelsdict = {\
	'A': '1985-2014',
	'B': '1955-1984',
	'C': '1982-2011',
	'D': '1982-1991'
}

for label in ['A', 'B', 'C', 'D']:

	period = labelsdict[label]

	df = pd.read_csv('./data/sample.csv')

	df1 = pd.read_csv('./data/socioeconomic_fd_NS.csv'); df1['diff'] = 'NS'
	df2 = pd.read_csv('./data/socioeconomic_fd_WE.csv'); df2['diff'] = 'WE'
	dfs = pd.concat([df1, df2], ignore_index=True, axis=0)

	df1 = pd.read_csv('./data/geography_fd_NS.csv'); df1['diff'] = 'NS'
	df2 = pd.read_csv('./data/geography_fd_WE.csv'); df2['diff'] = 'WE'
	dfg = pd.concat([df1, df2], ignore_index=True, axis=0)

	df1 = pd.read_csv('./data/nightlights_fd_NS.csv'); df1['diff'] = 'NS'
	df2 = pd.read_csv('./data/nightlights_fd_WE.csv'); df2['diff'] = 'WE'
	dfn = pd.concat([df1, df2], ignore_index=True, axis=0)

	df1 = pd.read_csv('./data/climate_{0:s}_fd_NS.csv'.format(period)); df1['diff'] = 'NS'
	df2 = pd.read_csv('./data/climate_{0:s}_fd_WE.csv'.format(period)); df2['diff'] = 'WE'

	variables = ['T_mean', 'T_mean_sq', 'T_range', 'T_ds_bystd', 'T_ac_bdstd']
	lag = 1
	for var in variables:
		df1['{0:s}_lag{1:d}'.format(var, lag)] = df1.sort_values(by='latitude', ascending=False).groupby('longitude')[var].shift(lag)
		df2['{0:s}_lag{1:d}'.format(var, lag)] = df2.sort_values(by='longitude', ascending=True).groupby('latitude')[var].shift(lag)

	dfc = pd.concat([df1, df2], ignore_index=True, axis=0)

	df = df.merge(dfs, on=['longitude', 'latitude'], how='left')
	df = df.merge(dfg, on=['longitude', 'latitude', 'diff'], how='left')
	df = df.merge(dfn, on=['longitude', 'latitude', 'diff'], how='left')
	df = df.merge(dfc, on=['longitude', 'latitude', 'diff'], how='left')

	### ==========================================

	df = df.rename(columns={'CNTR_CODE': 'BORDER_FE'})
	df['BORDER_FE'] = df['BORDER_FE'].astype(str)

	dfs = pd.read_csv('./data/socioeconomic.csv')
	dfs = dfs.loc[:, ['longitude', 'latitude', 'CNTR_CODE', 'urban05', 'urban20', 'urban50', 'urban05.20', 'urban20.50']]
	df = df.merge(dfs, on=['latitude', 'longitude'], how='left')

	dft = pd.read_csv('./data/temperature_bins.csv')
	df = df.merge(dft, on=['latitude', 'longitude'], how='left')

	### ==========================================

	dfs = pd.read_csv('./data/standard_deviations.csv', names=['variable', 'std']).set_index('variable')

	variables = ['log_nightlight_normed', 'log_nightlight_normed_v2',
				'hsin_nightlight_normed', 'log_nightlight_normed_v2_20152019',
				'T_mean', 'T_range', 'T_std', 'T_ds_bystd', 'T_ac_bdstd', 'P_mean',
				'r_mean', 'ssrd_mean', 'P_std', 'P_bystd',
				'coastal_distances', 'water_distances', 'elevation', 'ruggedness',
				'cropland_proportion', 'pasture_proportion',
				'T_mean_lag1', 'T_range_lag1', 'T_ds_bystd_lag1', 'T_ac_bdstd_lag1']
	variables_sq = ['T_mean_sq', 'P_mean_sq', 'r_mean_sq', 'ssrd_mean_sq',
				'coastal_distances_sq', 'water_distances_sq', 'elevation_sq', 'ruggedness_sq',
				'cropland_proportion', 'pasture_proportion',
				'T_mean_sq_lag1', ]

	if label in ['C', 'D']:
		variables = variables + [\
				'log_nightlight_normed_F101992',
				'log_nightlight_normed_F182012',
				'g_F182012vsF101992']

	if label in ['A']:
		variables = variables + [\
				'logPOPULATION_DENSITY_2015']

	for variable in variables:
		df[variable] = df[variable] / dfs.loc[variable.replace('_lag1', ''), 'std']

	for variable in variables_sq:
		df[variable] = df[variable] / (dfs.loc[variable.replace('_lag1', '').replace('_sq', ''), 'std'] ** 2.)

	### ==========================================

	df.to_csv('./data/data_combined_{0:s}.csv'.format(label))

	### ==========================================

	if label == 'A':

		for j, sublabel in enumerate(['a']):

			df = df.drop(columns=[c for c in df.columns if (c[:3] == 'bin')])
			bins = ['2Ca'][j]
			ifile = 'era5_1985-2014_t2m_{0:s}_allbins_mean.csv'.format(bins)
			df1 = pd.read_csv('./data/' + ifile.replace('.csv', '_fd_NS.csv')); df1['diff'] = 'NS'
			df2 = pd.read_csv('./data/' + ifile.replace('.csv', '_fd_WE.csv')); df2['diff'] = 'WE'
			dfb = pd.concat([df1, df2], ignore_index=True, axis=0)
			df = df.merge(dfb, on=['latitude', 'longitude', 'diff'], how='left')

			df.to_csv('./data/data_combined_{0:s}{1:s}.csv'.format(label, sublabel))

### ====================================================================================
## long differences

TIME_PERIOD_1 = '1982-1991'
TIME_PERIOD_2 = '2002-2011'

ifile = 'sample.csv'
datapath = './data/'
df = pd.read_csv(os.path.join(datapath, ifile))

ifile = 'nightlights.csv'
datapath = './data/'
dfn = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(dfn, on=['latitude', 'longitude'], how='left')

ifile = 'socioeconomic.csv'
datapath = './data/'
dfs = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(dfs, on=['latitude', 'longitude'], how='left')

ifile = 'climate_ld_{0:s}vs{1:s}.csv'.format(TIME_PERIOD_2, TIME_PERIOD_1)
datapath = './data/'
dfl = pd.read_csv(os.path.join(datapath, ifile))

df = df.merge(dfl, on=['latitude', 'longitude'], how='left')

dfs = pd.read_csv('./data/standard_deviations.csv', names=['variable', 'std']).set_index('variable')

variables = [\
			'g_F182012vsF101992', 
			'T_mean',
			'T_range', 'T_ds_bystd', 'T_ac_bdstd',
			'P_mean',
			'r_mean', 'ssrd_mean',
			'P_std', 'P_bystd']
variables_sq = ['T_mean_sq', 'P_mean_sq', 'r_mean_sq', 'ssrd_mean_sq']

for variable in variables:
	df[variable] = df[variable] / dfs.loc[variable.replace('_lag1', ''), 'std']

for variable in variables_sq:
	df[variable] = df[variable] / (dfs.loc[variable.replace('_lag1', '').replace('_sq', ''), 'std'] ** 2.)

dft = pd.read_csv('./data/temperature_bins.csv')
df = df.merge(dft, on=['latitude', 'longitude'], how='left')

df.to_csv('./data/data_combined_{0:s}.csv'.format('E'))


### ====================================================================================
## cross section

ifile = 'sample.csv'
datapath = './data/'
df = pd.read_csv(os.path.join(datapath, ifile))

ifile = 'nightlights.csv'
datapath = './data/'
dfn = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(dfn, on=['latitude', 'longitude'], how='left')

ifile = 'geography.csv'
datapath = './data/'
dfg = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(dfg, on=['latitude', 'longitude'], how='left')

ifile = 'socioeconomic.csv'
datapath = './data/'
dfs = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(dfs, on=['latitude', 'longitude'], how='left')

ifile = 'climate_1985-2014.csv'
datapath = './data/'
dfc = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(dfc, on=['latitude', 'longitude'], how='left')

columns_squared = [\
	'coastal_distances',
	'water_distances',
	'ruggedness',
	'elevation'
	]

for column in columns_squared:
	df[column + '_sq'] = df[column] ** 2.


dfs = pd.read_csv('./data/standard_deviations.csv', names=['variable', 'std']).set_index('variable')

variables = ['log_nightlight_normed',
			'hsin_nightlight_normed', 'log_nightlight_normed_v2_20152019',
			'T_mean', 'T_range', 'T_std', 'T_ds_bystd', 'T_ac_bdstd', 'P_mean',
			'r_mean', 'ssrd_mean', 'P_std', 'P_bystd',
			'coastal_distances', 'water_distances', 'elevation', 'ruggedness',
			'cropland_proportion', 'pasture_proportion']
variables_sq = ['T_mean_sq', 'P_mean_sq', 'r_mean_sq', 'ssrd_mean_sq',
				'coastal_distances_sq', 'water_distances_sq', 'elevation_sq', 'ruggedness_sq',
				'cropland_proportion', 'pasture_proportion']

for variable in variables:
	df[variable] = df[variable] / dfs.loc[variable.replace('_lag1', ''), 'std']

for variable in variables_sq:
	df[variable] = df[variable] / (dfs.loc[variable.replace('_lag1', '').replace('_sq', ''), 'std'] ** 2.)

df.to_csv('./data/data_combined_{0:s}.csv'.format('CS'))
