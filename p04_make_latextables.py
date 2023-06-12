#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from copy import deepcopy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator, LinearLocator

from scipy.stats import t 

## ===== define some functions ===== ##

def get_stars(p, mode=1):
	#return ''

	if mode == 0:
		if p < 0.001:
			return '$^{* * *}$'
		elif p < 0.01:
			return '$^{* *}$'
		elif p < 0.05:
			return '$^{*}$'
		else:
			return ''
	elif mode == 1:
		if p < 0.01:
			return '$^{* * *}$'
		elif p < 0.05:
			return '$^{* *}$'
		elif p < 0.1:
			return '$^{*}$'
		else:
			return ''

var2name = {\
				'T_ac_bdstd': 'Day-to-day variab. of $T$',
				'T_range': 'Seasonal variab. of $T$',
				'T_mean_ge20False:T_ds_bystd': 'Interann. variab. of $T$ $*$ $\delta(\overline{T} < 20)$',
				'T_mean_ge20True:T_ds_bystd': 'Interann. variab. of $T$ $*$ $\delta(\overline{T} \ge 20)$',
				'T_mean': 'Annual mean temperature',
				'T_mean_sq': 'Annual mean temperature sq',
				'P_mean': 'Precipitation $P$',
				'r_mean': 'Relative humidity',
				'ssrd_mean': 'Solar radiation',
				'P_mean_sq': 'Precipitation sq',
				'r_mean_sq': 'Relative humidity sq',
				'ssrd_mean_sq': 'Solar radiation sq',
				'P_std': 'Seasonal variability of $P$',
				'P_bystd': 'Interannual variability of $P$',
				'coastal_distances': 'Distance from nearest coast',\
				'coastal_distances_sq': 'Distance from nearest coast sq',\
				'water_distances': 'Distance from nearest lake/river',\
				'water_distances_sq': 'Distance from nearest lake/river sq',\
				'elevation': 'Elevation',\
				'elevation_sq': 'Elevation sq',\
				'ruggedness': 'Ruggedness',\
				'ruggedness_sq': 'Ruggedness sq',\
				'cropland_proportion': 'Share of cropland',
				'pasture_proportion': 'Share of pasture',
				'log_nightlight_normed_F101992': 'Nightlights in 1992',
				'(Intercept)': '(Intercept)',
				'empty': ''
}

def get_dataframe(df, index_col_est, index_col_se, index_col_p, model_name='Model X'):
	columns = df.columns
	df = df.iloc[:, [0, index_col_est, index_col_se, index_col_p]].rename(columns={'Unnamed: 0': 'Variable',
						columns[index_col_est]: 'Estimate', columns[index_col_se]: 'SE', columns[index_col_p]: 'P'})
	df_new = df.iloc[np.repeat(np.arange(len(df)), 2)].reset_index(drop=True)

	# remove variable label from every second column
	df_new.loc[np.arange(1, df_new.shape[0], 2), 'Variable'] = df_new.loc[np.arange(1, df_new.shape[0], 2), 'Variable'] + '_SE'

	# correct for number of figures to show
	df_new.loc[:, 'Estimate'] = df_new.apply(lambda x: '{0:5.4f}{1:s}'.format(x['Estimate'], get_stars(x['P'])), axis=1)
	df_new.loc[:, 'SE'] = df_new['SE'].apply(lambda x: '({0:5.4f})'.format(x))

	# copy in SE in every second row
	df_new.loc[np.arange(1, df_new.shape[0], 2), 'Estimate'] = df_new.loc[np.arange(1, df_new.shape[0], 2), 'SE']

	# rename column
	df_new = df_new.rename(columns={'Estimate': model_name})

	return df_new[['Variable', model_name]]

def sort_variables(df, var2name):
	df['var_sort'] = df['Variable']
	categories_estimates = list(var2name.keys())
	categories_SE = [c + '_SE' for c in categories_estimates]
	categories_all = [None]*(len(categories_estimates)+len(categories_SE))
	categories_all[::2] = categories_estimates
	categories_all[1::2] = categories_SE
	df['var_sort'] = pd.Categorical(
	    df['var_sort'], 
	    categories=categories_all, 
	    ordered=True
	)
	df = df.sort_values(by='var_sort', ignore_index=True)
	df = df.drop(columns=['var_sort'])
	return df


for TABLE_ID in ['01', '02', '03', '04', '05']:#, '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17']:
	MULTIPLE_SE = False
	OVB_STATS = False
	REMOVE_CONTROLS = False
	REMOVE_BIN_INTERCEPTS = True
	ADD_SCALED_COEFFS = False
	DEPVAR = 'nl'

	# illustration of SFD
	if TABLE_ID == '01':
		EXPERIMENTS = ['CS01a', 'CS02a', 'CS01b', 'CS02b', 'FD01', 'FD02']
		COLUMN_NAMES = [str(i+1) for i in range(np.size(EXPERIMENTS))]
		INDEX_COL_EST = 1
		INDEX_COL_SE = 2
		INDEX_COL_P = 3
		ADD_SCALED_COEFFS = False
		ADD_GDP_COEFFS = False

	# main results
	elif TABLE_ID == '02':
		EXPERIMENTS = ['A01', 'A01b', 'A01a']
		COLUMN_NAMES = [str(i+1) for i in range(np.size(EXPERIMENTS))]
		INDEX_COL_EST = 1
		INDEX_COL_SE = 2
		INDEX_COL_P = 3
		ADD_SCALED_COEFFS = True

	# reverse causality
	elif TABLE_ID == '03':
		EXPERIMENTS = ['C01', 'D01a', 'D01b']
		COLUMN_NAMES = [str(i+1) for i in range(np.size(EXPERIMENTS))]
		INDEX_COL_EST = 1
		INDEX_COL_SE = 2
		INDEX_COL_P = 3
		ADD_SCALED_COEFFS = True

	# population
	elif TABLE_ID == '04':
		EXPERIMENTS = ['A05a', 'A05b', 'A05c']
		COLUMN_NAMES = [str(i+1) for i in range(np.size(EXPERIMENTS))]
		INDEX_COL_EST = 1
		INDEX_COL_SE = 2
		INDEX_COL_P = 3
		ADD_SCALED_COEFFS = True

	# agriculture
	elif TABLE_ID == '05':
		EXPERIMENTS = ['A04a', 'A04b', 'A04c']
		COLUMN_NAMES = [str(i+1) for i in range(np.size(EXPERIMENTS))]
		INDEX_COL_EST = 1
		INDEX_COL_SE = 2
		INDEX_COL_P = 3
		ADD_SCALED_COEFFS = True

	else:
		continue

	df_all = pd.DataFrame(columns=['Variable'])

	for i, EXPERIMENT in enumerate(EXPERIMENTS):

		print(EXPERIMENT)

		COLUMN_NAME = COLUMN_NAMES[i]

		# read in regression results as data frame
		datapath = './results/'
		ifile = 'coeffs_{0:s}.csv'.format(EXPERIMENT)
		df = pd.read_csv(os.path.join(datapath, ifile))

		# transform data frame to get all information in one column
		df_new = get_dataframe(df, index_col_est=INDEX_COL_EST, index_col_se=INDEX_COL_SE, index_col_p=INDEX_COL_P, model_name=COLUMN_NAME)

		# read in R2 and other statistics
		datapath = './results/'
		ifile = 'coeffs_{0:s}.csv'.format(EXPERIMENT)
		df = pd.read_csv(os.path.join(datapath, ifile))

		# add empty line
		df_new = df_new.append({'Variable': 'empty'}, ignore_index=True)
		df_new = df_new.append({'Variable': 'R2', COLUMN_NAME: '{0:5.4f}'.format(df['rsquared'].values[0])}, ignore_index=True)
		df_new = df_new.append({'Variable': 'N', COLUMN_NAME: '{0:5d}'.format(df['N'].values[0])}, ignore_index=True)
		
		# add column of this model to dataframe, merging on variables
		df_all = df_all.merge(df_new, on=['Variable'], how='outer')

	var2name_plus = deepcopy(var2name)
	variables = [variable for variable in df_all['Variable'].unique() if '_SE' not in variable]
	for variable in variables:
		if variable not in var2name.keys():
			var2name_plus[variable] = variable.replace('_', '.')

	var2name_plus_stats = {**var2name_plus,
							'rsquared': 'R2',
							'R2 adj.': 'R2 adj.',
							'df': 'df',
							'N': 'N',
							'$R^{2}_{Y\\sim D|X}$ (\\%)': '$R^{2}_{Y\\sim D|X}$ (\\%)',
							'$RV$': '$RV$',
							'$RV_{\\alpha}$': '$RV_{\\alpha}$'}

	df_all = sort_variables(df_all, var2name_plus_stats)

	# replace variable names
	index_SE = (df_all['Variable'].str.contains('_SE'))
	df_all.loc[index_SE, 'Variable'] = ''
	df_all.loc[~index_SE, 'Variable'] = df_all.loc[~index_SE, 'Variable'].apply(lambda x: var2name_plus_stats.get(x, x))

	# ===========
	if ADD_SCALED_COEFFS == True:

		# add translation into 'log points per degree C'
		df_coeffs = df_all.loc[~(df_all['Variable'].isin(['', 'R2', 'df']) | df_all['Variable'].str.contains('controls')), :].reset_index(drop=True)
		df_coeffs.index = df_coeffs['Variable'].values

		scaling = pd.read_csv('./data/standard_deviations.csv')
		scaling.columns = ['var', 'sd']

		scaling_nl = scaling.loc[scaling.iloc[:, 0] == 'log_nightlight_normed', 'sd'].values
		scaling_pd = scaling.loc[scaling.iloc[:, 0] == 'logPOPULATION_DENSITY_2015', 'sd'].values

		scaling_vars = scaling.loc[scaling.iloc[:, 0].isin(var2name.keys()), :]
		scaling_vars['Variable'] = scaling_vars.iloc[:, 0].apply(lambda x: var2name[x])
		scaling_vars.index = scaling_vars['Variable'].values

		def remove_stars(x):
			if '$' in str(x):
				return float(x.split('$')[0])
			else:
				return float(x)

		for col in df_coeffs.columns[1:]:
			df_coeffs[col] = df_coeffs[col].apply(lambda x: remove_stars(x))
		for i, var in enumerate(df_coeffs.index):
			var = var.split(' $*$')[0]
			if DEPVAR == 'nl':
				if var in scaling_vars.index.values:
					df_coeffs.iloc[i, 1:] = (df_coeffs.iloc[i, 1:].values / scaling_vars.loc[var, 'sd']) * scaling_nl
			else:
				for j, depvar in enumerate(DEPVAR):
					if depvar == 'nl':
						scaling = scaling_nl
					else:
						scaling = scaling_pd
					df_coeffs.iloc[i, 1+j] = (df_coeffs.iloc[i, 1+j] / scaling_vars.loc[var, 'sd']) * scaling
		for col in df_coeffs.columns[1:]:
			df_coeffs[col] = df_coeffs[col].apply(lambda x: '{0:5.4f}'.format(x))
		df_all = pd.concat([df_all.iloc[:-2], df_coeffs, df_all.iloc[-2:]], ignore_index=True)

		# ===========

		if ADD_GDP_COEFFS:

			df_elasticities1 = pd.read_csv('./results/coeffs_A12a.csv')
			df_elasticities1 = df_elasticities1.set_index(df_elasticities1.iloc[:, 0]).iloc[:, 1]
			df_elasticities2 = pd.read_csv('./results/coeffs_A12b.csv')
			df_elasticities2 = df_elasticities2.set_index(df_elasticities2.iloc[:, 0]).iloc[:, 1]
			df_elasticities = pd.concat([df_elasticities1, df_elasticities2], axis=0)

			for i, var in enumerate(df_coeffs.index):
				var = var.split(' $*$')[0]
				if var in ['Day-to-day variab. of $T$', 'Seasonal variab. of $T$']:
					elasticity = df_elasticities.loc['log_nightlight_normed']
				elif var == 'Interann. variab. of $T$ $*$ $\delta(\overline{T} < 20)$':
					elasticity = df_elasticities.loc['T_mean_ge20False:log_nightlight_normed']
				elif var == 'Interann. variab. of $T$ $*$ $\delta(\overline{T} > 20)$':
					elasticity = df_elasticities.loc['T_mean_ge20True:log_nightlight_normed']
				else:
					elasticity = 0

				if DEPVAR == 'nl':
					if var in scaling_vars.index.values:
						df_coeffs.iloc[i, 1:] = (df_coeffs.iloc[i, 1:].values / scaling_vars.loc[var, 'sd']) * scaling_gdp
				else:
					print('Scaling not possible with GDP')
					break
			for col in df_coeffs.columns[1:]:
				df_coeffs[col] = df_coeffs[col].apply(lambda x: '{0:5.4f}'.format(x))
			df_all = pd.concat([df_all.iloc[:-2], df_coeffs, df_all.iloc[-2:]], ignore_index=True)

		# ===========

	tablepath = './tables'
	tablefile = 'table_results_{0:s}.tex'.format(TABLE_ID)
	#tablefile = 'table_' + '-'.join(EXPERIMENTS) + '.tex'
	#with open(os.path.join(tablepath, tablefile), 'w') as ofp:
	with pd.option_context("max_colwidth", 1000):
		df_all.to_latex(buf=os.path.join(tablepath, tablefile), index=False, encoding='utf-8', escape=False, column_format='l'+'r'*(df_all.shape[1]-1), na_rep='')

