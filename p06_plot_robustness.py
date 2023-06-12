#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import copy

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

### ====================================================================================

def extract_errorbar(dx, variable):
	y = dx.loc[variable, 'coef.model_fixest.']
	y_error = 1.96*dx.loc[variable, 'se']
	return y, y_error

colors = ['b', 'g', 'r', 'm']

variable_labels = {\
	'T_ac_bdstd': 'Day-to-day',
	'T_range': 'Seasonal',
	'T_mean_ge20False:T_ds_bystd': 'Interannual ($\overline{T}$ < 20)',
	'T_mean_ge20True:T_ds_bystd': 'Interannual ($\overline{T} \geq$ 20)'
}

dfs = pd.read_csv('./data/standard_deviations.csv', names=['variable', 'std']).set_index('variable')

### ====================================================================================
### bins

experiment = 'Aa01'
df = pd.read_csv('./results/coeffs_{0:s}.csv'.format(experiment))
df = df.set_index(df.columns[0])

variables = ['bin{0:02d}'.format(b) for b in range(0, 17+1, 1)]

fig, ax = plt.subplots(figsize=(10,5))

for i, variable in enumerate(variables):

	if variable in df.index.values:
		y, yerror = extract_errorbar(df, variable)
	else:
		y = 0.
		yerror= 0.
	y = y * dfs.loc['log_nightlight_normed', 'std'] * 10.
	yerror = yerror * dfs.loc['log_nightlight_normed', 'std'] * 10.
	ax.errorbar(i, y, yerror, markersize=5., capsize=4., elinewidth=2., marker='o', color='k')

ax.set_xticks(np.arange(1, i+1, 1)-0.5)
ax.set_xticklabels([str(0 + i * 2) for i in range(0, i, 1)])
xlims = ax.get_xlim()
ax.plot(xlims, [0., 0.], 'k-', lw=0.5)
ax.set_xlim(xlims)
ylims = ax.get_ylim()
ax.set_ylim(-np.max(np.abs(ylims)), np.max(np.abs(ylims)))
sns.despine(ax=ax, offset=1., right=True, top=True)
ax.set_xlabel('Daily mean temperature (degree Celsius)')
ax.set_ylabel('Change in log nightlights per 10 days in given bin\n relative to bin [10, 12)')
fig.savefig('./figures/coefficients_dailybins.pdf', bbox_inches='tight', transparent=True)

### ====================================================================================
### robustness plot

fig, axes = plt.subplots(figsize=(10,5), nrows=4, sharex=True, gridspec_kw={'hspace': 0.5})

experiments = ['A01', 'A01a', 'A01b',
				'A02a', 'A02b', # controls
				'A06', # arcsinh
				'A08', # season std
				'A07a', 'A07b', # nl v2, nl v2 average
				'B01', # earlier climate
				'A09', # spatial lag
				'A10', # drop extremes in treatment
				'Aa01' # with daily temperature bins
				]
variables = ['T_ac_bdstd', 'T_range', 'T_mean_ge20False:T_ds_bystd', 'T_mean_ge20True:T_ds_bystd']

for e, experiment in enumerate(experiments):

	for i, variable in enumerate(variables):

		if experiment == 'A08':
			variable = variable.replace('range', 'std')
		if experiment == 'A10':
			experiment = experiments[e] + {0: 'a', 1: 'b', 2: 'c'}[i]

		df = pd.read_csv('./results/coeffs_{0:s}.csv'.format(experiment))
		df = df.set_index(df.columns[0])
		y, yerror = extract_errorbar(df, variable)

		axes[i].errorbar(e, y, yerror, markersize=5., capsize=4., elinewidth=2., marker='o', color=colors[i])

axes[-1].set_xticks(np.arange(0, e+1, 1))
axes[-1].set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
							'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'][0:len(experiments)])
for i, ax in enumerate(axes):
	xlims = ax.get_xlim()
	ax.plot(xlims, [0., 0.], 'k-', lw=0.5)
	ax.set_xlim(xlims)
	ylims = ax.get_ylim()
	ax.set_ylim(-np.max(np.abs(ylims)), np.max(np.abs(ylims)))
	sns.despine(ax=ax, offset=1., right=True, top=True)
	ax.annotate(text='{0:s}'.format(variable_labels[variables[i]]), xy=(0.02, 1.02), xycoords='axes fraction', ha='left', va='bottom')
fig.savefig('./figures/coefficients_robustness.pdf', bbox_inches='tight', transparent=True)

### ====================================================================================
### population + long differences

fig, axes = plt.subplots(figsize=(10,5), nrows=4, sharex=True, gridspec_kw={'hspace': 0.5})

experiments = ['A01',
				'A11b', # population as dependent variable
				'A11a', # controlling for population
				'E01', # long diff
				]
variables = ['T_ac_bdstd', 'T_range', 'T_mean_ge20False:T_ds_bystd', 'T_mean_ge20True:T_ds_bystd']

xticks = []
for e, experiment in enumerate(experiments):

	for i, variable in enumerate(variables):

		if experiment == 'A08':
			variable = variable.replace('range', 'std')
		if experiment == 'A10':
			experiment = experiments[e] + {0: 'a', 1: 'b', 2: 'c'}[i]

		df = pd.read_csv('./results/coeffs_{0:s}.csv'.format(experiment))
		df = df.set_index(df.columns[0])
		y, yerror = extract_errorbar(df, variable)

		if e > 0:
			x = e + 0.5
		else:
			x = e
		if e > 2:
			x = x + 0.5
		axes[i].errorbar(x, y, yerror, markersize=5., capsize=4., elinewidth=2., marker='o', color=colors[i])
	xticks.append(x)

axes[-1].set_xticks(xticks)
axes[-1].set_xticklabels(['a', 'b', 'c', 'd'])
for i, ax in enumerate(axes):
	ax.set_xlim([-1, 5.])
	xlims = ax.get_xlim()
	ax.plot(xlims, [0., 0.], 'k-', lw=0.5)
	ax.set_xlim(xlims)
	ylims = ax.get_ylim()
	ax.set_ylim(-np.max(np.abs(ylims)), np.max(np.abs(ylims)))
	ylims = ax.get_ylim()
	ax.plot([0.75, 0.75], ylims, 'k--', lw=1.)
	ax.plot([3.25, 3.25], ylims, 'k--', lw=1.)
	sns.despine(ax=ax, offset=1., right=True, top=True)
	ax.annotate(text='{0:s}'.format(variable_labels[variables[i]]), xy=(0.02, 1.02), xycoords='axes fraction', ha='left', va='bottom')
fig.savefig('./figures/coefficients_combined.pdf', bbox_inches='tight', transparent=True)

