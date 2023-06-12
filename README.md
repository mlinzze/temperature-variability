Overview
--------

The code in this replication package can be used to reproduce the results published in [Linsenmeier, M. (2023): Temperature variability and long-run economic development. Journal of Environmental Economics and Management.](https://mlinsenmeier.com/research/).

The package consists of several scripts in Python and one script in R. To run these scripts, the original data must be downloaded first from [Zenodo](10.5281/zenodo.8030398) and deposited in a subfolder `Data`.

Computational requirements
---------------------------

### Software Requirements

- Python 3.10.9
  - `numpy` 1.23.4
  - `pandas` 1.5.1
  - `scipy` 1.10.0
  - `statsmodels` 0.13.5
  - `geopandas` 0.12.0
  - `newtorkx` 3.0
  - `matplotlib` 3.6.1
  - `seaborn` 0.12.0
- R
  - fixest

The file `requirements.txt` lists these dependencies, please run `pip install -r requirements.txt` as the first step. See [https://pip.readthedocs.io/en/1.1/requirements.html](https://pip.readthedocs.io/en/1.1/requirements.html) for further instructions on using the `requirements.txt` file.

### Memory and Runtime Requirements

Approximate time needed on a standard (2023) desktop machine:
- empirical analysis : 1 hour
- simulations: 7 days (can be shortened by reducing the number of Monte Carlo simulations)

Description of individual scripts
----------------------------

- `stata_all.do`: This script estimates all proportional hazard models and stores the results (estimated coefficients and predicted effects) in the folder `results`.
- `p01_make_latextables.py`: This script uses the estimated coefficients and produces all regression tables shown in the paper and SI.
- `p02_examine_nonlinearities.py`: This script visualises the predicted effects of the non-linear models and then fits an inverse hyperbolic sinus to the model with cubic splines.
- `p03_quantify_emission-reductions.py`: This script uses the results of the Monte Carlo simulations and quantifies the direct and indirect emission reductions from policy diffusion.
- `p04a_visualise_emission_reductions.py`: This script visualises the direct and indirect emission reductions.
- `p04b_visualise_centrality.py`: This script calculates network centrality measures for all countries, regresses indirect emission reductions on those measures, and visualises the statistical associations with scatter plots.
- `p04c_visualise_coverage.py`: This script visualises the results of the Monte Carlo simulations including the sensitivity analysis in terms of the share of countries/global emissions with a carbon pricing policy for scenarios with and without policy diffusion.
- `p04c_visualise_effectivenes.py`: This script visualises the indirect emission reductions for different assumptions about the effectiveness of carbon pricing policies.

### License for Code

The code in this repository is licensed under a CC-BY-NC license.

Instructions to Replicators
---------------------------

- Run all scripts in the order indicated by the file names (i.e. `p01`, `p02`, `p03`, ...). This can also be achieved with the Makefile in the repository (`make clean; make all`).
- Some of the scripts store intermediate results in the folder `results`.
- Once all scripts have finished, all tables and figures can be found in the respective folders `tables` and `figures`.
- For the simulations, see the separate Makefile in the folder `simulations`.
