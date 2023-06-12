## ==================================================================================

library(fixest)

## ==================================================================================
## comparison of estimation strategies

#if (FALSE) { #SWITCH

df <- read.csv("./data/data_combined_CS.csv")
df$CNTR_CODE <- as.factor(df$CNTR_CODE)

model_fixest <- feols(log_nightlight_normed ~ 
		T_ac_bdstd, df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_CS01a.csv')

model_fixest <- feols(log_nightlight_normed ~ 
		T_ac_bdstd
		| CNTR_CODE, df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_CS01b.csv')

model_fixest <- feols(log_nightlight_normed ~ 
		T_ac_bdstd + T_mean, df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_CS02a.csv')

model_fixest <- feols(log_nightlight_normed ~ 
		T_ac_bdstd + T_mean 
		| CNTR_CODE, df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_CS02b.csv')

## ==================================================================================

df <- read.csv("./data/data_combined_A.csv")
df$BORDER_FE <- as.factor(df$BORDER_FE)
df$CNTR_CODE <- as.factor(df$CNTR_CODE)
df$T_mean_ge20 <- as.factor(df$T_mean_ge20)
df$T_mean_c5 <- as.factor(df$T_mean_c5)
df$T_mean_c4 <- as.factor(df$T_mean_c4)

## ==================================================================================

model_fixest <- feols(log_nightlight_normed ~ 
		T_ac_bdstd
		| BORDER_FE, df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_FD01.csv')

model_fixest <- feols(log_nightlight_normed ~ 
		T_ac_bdstd + T_mean  
		| BORDER_FE, df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_FD02.csv')

## ==================================================================================
## parsimonious model

## pooled
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A01.csv')

## NS
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[df$diff == 'NS', ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A01a.csv')

## WE
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[df$diff == 'WE', ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A01b.csv')

## ============================================
## control variables

## only linear
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A02a.csv')

## bins
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		T_mean_c5 : T_mean + 
		T_mean_c5 : P_mean + 
		T_mean_c5 : r_mean + 
		T_mean_c5 : P_std + 
		T_mean_c5 : P_bystd + 
		T_mean_c5 : coastal_distances + 
		T_mean_c5 : water_distances + 
		T_mean_c5 : elevation + 
		T_mean_c5 : ruggedness
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A02b.csv')

## ==================================================================================
## binned model

model_fixest <- feols(log_nightlight_normed ~ 
		T_mean_c4 +
		T_mean_c4 : T_mean +
		T_mean_c4 : T_range + T_mean_c4 : T_ds_bystd + T_mean_c4 : T_ac_bdstd +
		P_mean + 
		r_mean + 
		P_std + 
		P_bystd + 
		coastal_distances + 
		water_distances + 
		elevation + 
		ruggedness
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A03.csv')

## =========================================
## agriculture

## only agriculture
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq +
		cropland_proportion
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A04a.csv')

## only pasture
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq +
		pasture_proportion
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A04b.csv')

## both
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq +
		cropland_proportion + pasture_proportion
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A04c.csv')

## =========================================
## urban versus rural

model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[df$urban05 == 'True', ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A05a.csv')

model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[df$urban05.20 == 'True', ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A05b.csv')

model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[df$urban50 == 'True', ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A05c.csv')


## =========================================
## arcsinh transformation

model_fixest <- feols(hsin_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A06.csv')

## =========================================
## nightlights v2 and v2 average

model_fixest <- feols(log_nightlight_normed_v2 ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A07a.csv')

model_fixest <- feols(log_nightlight_normed_v2_20152019 ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A07b.csv')

## =========================================
## seasonal std

model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_std + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A08.csv')

## =========================================
## spatial lag

model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq +
		T_mean_lag1 + T_mean_sq_lag1 +
		T_range_lag1 + T_mean_ge20 : T_ds_bystd_lag1 + T_ac_bdstd_lag1
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A09.csv')

## =========================================
## drop largest differences

# day to day
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq 	+ ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[(df$T_ac_bdstd > quantile(df$T_ac_bdstd, c(0.05), na.rm=TRUE)) & (df$T_ac_bdstd < quantile(df$T_ac_bdstd, c(0.95), na.rm=TRUE)), ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A10a.csv')

# seasonal
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[(df$T_range > quantile(df$T_range, c(0.05), na.rm=TRUE)) & (df$T_range < quantile(df$T_range, c(0.95), na.rm=TRUE)), ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A10b.csv')

# interannual
model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df[(df$T_ds_bystd > quantile(df$T_ds_bystd, c(0.05), na.rm=TRUE)) & (df$T_ds_bystd < quantile(df$T_ds_bystd, c(0.95), na.rm=TRUE)), ], cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A10c.csv')

## =========================================
## earlier climate data

df <- read.csv("./data/data_combined_B.csv")
df$BORDER_FE <- as.factor(df$BORDER_FE)
df$CNTR_CODE <- as.factor(df$CNTR_CODE)
df$T_mean_ge20 <- as.factor(df$T_mean_ge20)
df$T_mean_c5 <- as.factor(df$T_mean_c5)

model_fixest <- feols(log_nightlight_normed ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_B01.csv')

## =========================================
## reverse causality

df <- read.csv("./data/data_combined_C.csv")
df$BORDER_FE <- as.factor(df$BORDER_FE)
df$CNTR_CODE <- as.factor(df$CNTR_CODE)
df$T_mean_ge20 <- as.factor(df$T_mean_ge20)
df$T_mean_c5 <- as.factor(df$T_mean_c5)

model_fixest <- feols(log_nightlight_normed_F182012 ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_C01.csv')

df <- read.csv("./data/data_combined_D.csv")
df$BORDER_FE <- as.factor(df$BORDER_FE)
df$CNTR_CODE <- as.factor(df$CNTR_CODE)
df$T_mean_ge20 <- as.factor(df$T_mean_ge20)
df$T_mean_c5 <- as.factor(df$T_mean_c5)

model_fixest <- feols(g_F182012vsF101992 ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_D01a.csv')

model_fixest <- feols(g_F182012vsF101992 ~ 
		log_nightlight_normed_F101992 +
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_D01b.csv')

## =========================================
## long-difference model

df <- read.csv("./data/data_combined_E.csv")
df$CNTR_CODE <- as.factor(df$CNTR_CODE)
df$T_mean_ge20 <- as.factor(df$T_mean_ge20)
df$T_mean_c5 <- as.factor(df$T_mean_c5)

model_fixest <- feols(g_F182012vsF101992 ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_E01.csv')

#} #SWITCH

## =========================================
## extreme events / nonlinear effects of levels

df <- read.csv("./data/data_combined_Aa.csv")
df$CNTR_CODE <- as.factor(df$CNTR_CODE)
df$T_mean_ge20 <- as.factor(df$T_mean_ge20)
df$T_mean_c5 <- as.factor(df$T_mean_c5)

model_fixest <- feols(log_nightlight_normed ~ 
		bin00 + bin01 + bin02 + bin03 + bin04 + bin05 + bin07 + bin08 + 
		bin09 + bin10 + bin11 + bin12 + bin13 + bin14 + bin15 + bin16 + bin17 + # bin6 is [10, 12]
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq + ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_Aa01.csv')

## =========================================
## population

df <- read.csv("./data/data_combined_A.csv")
df$BORDER_FE <- as.factor(df$BORDER_FE)
df$CNTR_CODE <- as.factor(df$CNTR_CODE)
df$T_mean_ge20 <- as.factor(df$T_mean_ge20)
df$T_mean_c5 <- as.factor(df$T_mean_c5)

model_fixest <- feols(log_nightlight_normed ~ 
		logPOPULATION_DENSITY_2015 +
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq 	+ ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A11a.csv')

model_fixest <- feols(logPOPULATION_DENSITY_2015 ~ 
		T_mean + T_mean_sq +
		T_mean_ge20 +
		T_range + T_mean_ge20 : T_ds_bystd + T_ac_bdstd +
		P_mean + r_mean + ssrd_mean +
		P_mean_sq + r_mean_sq 	+ ssrd_mean_sq +
		P_std + P_bystd + 
		coastal_distances + water_distances + elevation + ruggedness +
		coastal_distances_sq + water_distances_sq + elevation_sq + ruggedness_sq
		| BORDER_FE,
		df, cluster = ~CNTR_CODE)
summary(model_fixest, cluster = ~CNTR_CODE)
coeffs <- data.frame(coef(model_fixest))
coeffs$se <- se(model_fixest)
coeffs$p <- pvalue(model_fixest)
coeffs$N <- summary(model_fixest)$nobs
coeffs$rsquared <- r2(model_fixest, 'r2')
write.csv(data.frame(coeffs), './results/coeffs_A11b.csv')


