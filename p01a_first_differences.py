#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import copy

import numpy as np
import pandas as pd

### ==========================================

def first_diff(x, cyclical=False):
	y = x - np.roll(x, 1)
	if cyclical == False:
		y[0] = np.nan
	return y

def compare_factors(x1, x2):
	if pd.isnull(x1) or pd.isnull(x2):
		return np.nan
	if x1 == x2:
		return 'NODIFF'
	else:
		return str(x1) + '-' + str(x2)

def first_diff_factors(x, cyclical=False):
	y = copy.deepcopy(x)
	for i in range(np.size(x)):
		if i == 0:
			if cyclical == True:
				y[i] = compare_factors(x[i], x[-1])
			else:
				y[i] = np.nan
		else:
			y[i] = compare_factors(x[i], x[i-1])
	return y

def first_difference(df, columns_continuous, columns_factors, direction, resolution):
	if direction == 'NS':
		dimensions = ['longitude', 'latitude']
		sort_ascending = [True, False]
		step = -1 * resolution
	if direction == 'WE':
		dimensions = ['latitude', 'longitude']
		sort_ascending = [False, True]
		step = +1 * resolution
	dfd = df.sort_values(by=dimensions, ascending=sort_ascending)
	for variable in columns_continuous:
		dfd[variable] = dfd.groupby(dimensions[0])[variable].transform(lambda x: first_diff(x.values))
	for variable in columns_factors:
		dfd[variable] = dfd.groupby(dimensions[0])[variable].transform(lambda x: first_diff_factors(x.values))
	# drop differences across gaps in the data
	indices = dfd.groupby(dimensions[0])[dimensions[1]].transform(lambda x: first_diff(x.values)) == step
	dfd = dfd.loc[indices, dimensions + columns_continuous + columns_factors]
	return dfd

### ==========================================

ifile = 'sample.csv'
datapath = './data/'
df_sample = pd.read_csv(os.path.join(datapath, ifile))

### ==========================================

ifile = 'nightlights.csv'
datapath = './data/'
df = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(df_sample, on=['latitude', 'longitude'], how='right')

columns_continuous = [c for c in df.columns if c not in ['longitude', 'latitude']]
columns_factors = []
df_out = first_difference(df, columns_continuous, columns_factors, direction='NS', resolution=0.25)
df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_NS.csv')), index=False)

df_out = first_difference(df, columns_continuous, columns_factors, direction='WE', resolution=0.25)
df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_WE.csv')), index=False)

### ==========================================

ifile = 'geography.csv'
datapath = './data/'
df = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(df_sample, on=['latitude', 'longitude'], how='right')

columns_squared = [\
	'coastal_distances',
	'water_distances',
	'ruggedness',
	'elevation'
	]

for column in columns_squared:
	df[column + '_sq'] = df[column] ** 2.

columns_continuous = [c for c in df.columns if c not in ['longitude', 'latitude']]
columns_factors = []
df_out = first_difference(df, columns_continuous, columns_factors, direction='NS', resolution=0.25)
df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_NS.csv')), index=False)

df_out = first_difference(df, columns_continuous, columns_factors, direction='WE', resolution=0.25)
df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_WE.csv')), index=False)

### ==========================================

ifile = 'socioeconomic.csv'
datapath = './data/'
df = pd.read_csv(os.path.join(datapath, ifile))
df = df.merge(df_sample, on=['latitude', 'longitude'], how='right')

columns_continuous = ['logPOPULATION_DENSITY_2015']
columns_factors = ['CNTR_CODE', 'PRVNC_CODE']
df_out = first_difference(df, columns_continuous, columns_factors, direction='NS', resolution=0.25)
df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_NS.csv')), index=False)

df_out = first_difference(df, columns_continuous, columns_factors, direction='WE', resolution=0.25)
df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_WE.csv')), index=False)

### ==========================================

TIME_PERIODS = ['1955-1984', '1985-2014',
				'1982-1991', '1982-2011', '2002-2011']
for time_period in TIME_PERIODS:
	ifile = 'climate_{0:s}.csv'.format(time_period)
	datapath = './data/'
	df = pd.read_csv(os.path.join(datapath, ifile))
	df = df.merge(df_sample, on=['latitude', 'longitude'], how='right')

	columns_continuous = [c for c in df.columns if c not in ['longitude', 'latitude']]
	columns_factors = []
	df_out = first_difference(df, columns_continuous, columns_factors, direction='NS', resolution=0.25)
	df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_NS.csv')), index=False)

	df_out = first_difference(df, columns_continuous, columns_factors, direction='WE', resolution=0.25)
	df_out.to_csv(os.path.join(datapath, ifile.replace('.csv', '_fd_WE.csv')), index=False)

### ==========================================

for bins in ['2Ca']:
	ifile = 'era5_1985-2014_t2m_{0:s}_allbins_mean.csv'.format(bins)
	datapath = './data/'
	df = pd.read_csv(os.path.join(datapath, ifile))
	df = df.merge(df_sample, on=['latitude', 'longitude'], how='right')

	columns_continuous = [c for c in df.columns if c not in ['longitude', 'latitude']]
	columns_factors = []
	df_out = first_difference(df, columns_continuous, columns_factors, direction='NS', resolution=0.25)
	df_out.to_csv(os.path.join('./data/', ifile.replace('.csv', '_fd_NS.csv')), index=False)

	df_out = first_difference(df, columns_continuous, columns_factors, direction='WE', resolution=0.25)
	df_out.to_csv(os.path.join('./data/', ifile.replace('.csv', '_fd_WE.csv')), index=False)

