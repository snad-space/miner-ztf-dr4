# ZTF DR4 analysis

Here we do the analysis of ZTF DR4 datasets. A few points:
* The data itself is not present here due to large size.
* The scripts are located in [zwad repository](https://github.com/snad-space/zwad), so be sure to install it before digging here.
* The repository should be private for now, because... because.

## Data (temporial location)

### Features

All surves are extragalctic `|b| > 15°`, all light curves are "short" `58194.0 < MJD < 58664.0` and have at least 100 detections (in each passband for g+r)

- g+r, 13GB, 30M sources <http://sai.snad.space/tmp/dr4-features/extragal_short_gr_100.tar>
- g, 7GB, 33M sources <http://sai.snad.space/tmp/dr4-features/extragal_short_g_100.tar>
- r, 18GB, 83M sources <http://sai.snad.space/tmp/dr4-features/extragal_short_r_100.tar>

### SNANA sims (fakes)

Pickle files for `sim_fake/simulation_fake_features.ipynb` notebook, put them into `sim_fake/ztf_dr3_sim_data/ZTF_SIMS_ALLMODELS_3RD_RUN` directory. Each file is ~200MB

- <http://sai.snad.space/tmp/dr3-snana-sims/PALEO_ZTF_MODEL42_SNII-NMF.pkl.gz>
- <http://sai.snad.space/tmp/dr3-snana-sims/PALEO_ZTF_MODEL60_SLSN-I.pkl.gz>
- <http://sai.snad.space/tmp/dr3-snana-sims/PALEO_ZTF_MODEL62_SNIbc-MOSFIT.pkl.gz>
- <http://sai.snad.space/tmp/dr3-snana-sims/PALEO_ZTF_MODEL64_TDE.pkl.gz>
- <http://sai.snad.space/tmp/dr3-snana-sims/PALEO_ZTF_MODEL90_SNIa-SALT2.pkl.gz>
