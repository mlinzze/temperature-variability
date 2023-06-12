#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import copy

import numpy as np
import pandas as pd

### ==========================================

ifile = 'sample.csv'
datapath = './data/'
df = pd.read_csv(os.path.join(datapath, ifile))

### ==========================================

TIME_PERIOD_1 = '1982-1991'
TIME_PERIOD_2 = '2002-2011'

ifile = 'climate_{0:s}.csv'.format(TIME_PERIOD_1)
datapath = './data/'
df1 = pd.read_csv(os.path.join(datapath, ifile))

ifile = 'climate_{0:s}.csv'.format(TIME_PERIOD_2)
datapath = './data/'
df2 = pd.read_csv(os.path.join(datapath, ifile))

dfl = df1.merge(df2, on=['longitude', 'latitude'], suffixes=['_1', '_2'], how='left')
columns = ['T_mean', 'T_mean_sq',
			'T_range', 'T_ds_bystd', 'T_ac_bdstd',
			'P_mean', 'P_std', 'P_bystd',
			'r_mean', 'ssrd_mean',
			'P_mean_sq', 'r_mean_sq', 'ssrd_mean_sq']
for col in columns:
	dfl[col] = dfl[col + '_2'] - dfl[col + '_1']
dfl = dfl.loc[:, columns + ['latitude', 'longitude']]

df = df.merge(dfl, on=['latitude', 'longitude'], how='left')

ofile = 'climate_ld_{0:s}vs{1:s}.csv'.format(TIME_PERIOD_2, TIME_PERIOD_1)
df.to_csv('./data/{0:s}'.format(ofile), index=False)
