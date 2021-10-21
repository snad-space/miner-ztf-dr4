"""
Convert pickled file to readable dataframe
edited by patrickaleo
"""
import gzip
import pickle
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from astropy import table, coordinates, units as u
import sys

from .table import LSST_FILTERS


def read_data(filename):
    """Read data from pickled file to a pandas dataframe"""
    with gzip.open(filename, 'rb') as f:
        data = pickle.load(f)

    X = to_dataframe(data)
    y = pd.get_dummies(X.type == 0, prefix='SNIax', drop_first=True)
    X = X.drop(columns=['type'])

    return X, y


def to_dataframe(data):
    """Converts from a python dictionary to a pandas dataframe"""
    # For background noise. Add noise to better match real data
    # Background, mag units
    mag_backg = 20 # mag units
    sigma_mbackg = (0.0297*mag_backg-0.4179) # page 12, Malanchev et al. 2021, mag units
    # Background, flux units
    mu_fbackg = 10**(-0.4*(mag_backg-27.5)) # mean background, flux units 
    sigma_fbackg = 0.4*np.log(10) * mu_fbackg * sigma_mbackg # sigma background, flux units
    
    for idx in data:
        sn = data[idx]
        for filt in LSST_FILTERS:
            if np.array(sn[filt]['mjd']) is not None:
                sn['mjd_%s' % filt] = np.array(sn[filt]['mjd'])

                # For background noise. Add noise to better match real data
                rng = np.random.default_rng(42)
                flux_backg = rng.normal(mu_fbackg, sigma_fbackg)  # flux background
                
                # F = F_SNANA + F_background
                sn['fluxcal_%s' % filt] = np.array(sn[filt]['fluxcal']) + flux_backg 
                # sigma_F^2 = sigma_SNANA^2 +sigma_F,backg^2
                sn['fluxcalerr_%s' % filt] = np.sqrt(np.array(sn[filt]['fluxcalerr'])**2 + sigma_fbackg**2)

                # photflag
                sn['photflag_%s' % filt] = np.array(sn[filt]['photflag'])

                sn['photprob_%s' % filt] = np.array(sn[filt]['photprob'])

                sn['psf_sig1_%s' % filt] = np.array(sn[filt]['psf_sig1'])

                sn['sky_sig_%s' % filt] = np.array(sn[filt]['sky_sig'])

                sn['zeropt_%s' % filt] = np.array(sn[filt]['zeropt'])


                #make mag
                sn['mag_%s' % filt] = np.array(-2.5*np.log10(np.abs(sn[filt]['fluxcal'])))+27.5

                sn['snr_%s' % filt] = (sn['fluxcal_%s' % filt] / np.abs(sn['fluxcalerr_%s' % filt]))


                sn['magerr_%s' % filt] = np.array(1.086 / sn['snr_%s' % filt])
                sn['magerr_%s' % filt][sn['magerr_%s' % filt] > 0.5] = 0.5
                #  find cadence

                sn['delta_t_%s' % filt] = [j-i for i, j in zip(sn['mjd_%s' % filt][:-1], sn['mjd_%s' % filt][1:])]
                sn['median_delta_t_%s' % filt] = np.array(np.median(sn['delta_t_%s' % filt]))

                sn['magobs_%s' % filt] = np.array(np.median(sn['delta_t_%s' % filt]))


                # Mask to keep only  SNR >= 5 AND MAG BRIGHTER THAN 21.5 !!!
                # Although photflags are left, obs have added flux to make brighter and SNR.
                # SO SNR does not correspond to original photflag
                mask = (sn['snr_%s' % filt] >= 5) & (sn['mag_%s' % filt] <= 21.5) #& (sn['photflag_%s' % filt] != 0)
                sn['snr_%s' % filt] = sn['snr_%s' % filt][mask]
                sn['mag_%s' % filt] = sn['mag_%s' % filt][mask]
                sn['magerr_%s' % filt] = sn['magerr_%s' % filt][mask]
                sn['photflag_%s' % filt] = sn['photflag_%s' % filt][mask]
                sn['mjd_%s' % filt] = sn['mjd_%s' % filt][mask]
                sn['fluxcal_%s' % filt] = sn['fluxcal_%s' % filt][mask]
                sn['fluxcalerr_%s' % filt] = sn['fluxcalerr_%s' % filt][mask]

                # max fluxes
                if len(sn['fluxcal_%s' % filt]) > 0:
                    sn['maxfluxidx_%s' % filt] = np.argmax(sn['fluxcal_%s' % filt])
                    sn['maxflux_%s' % filt] = np.array(sn['fluxcal_%s' % filt][sn['maxfluxidx_%s' % filt]])
                    sn['maxfluxerr_%s' % filt] = np.array(sn['fluxcalerr_%s' % filt][sn['maxfluxidx_%s' % filt]])
                else:
                    sn['maxfluxidx_%s' % filt] = []
                    sn['maxflux_%s' % filt] = []
                    sn['maxfluxerr_%s' % filt] = []

                #find SNR at brightest epoch
                if sn['snr_%s' % filt].size > 0:
                    sn['max_epoch_%s' % filt] = np.min(sn['mag_%s' % filt])
                    max_mag_idx = (np.argmin(sn['mag_%s' % filt]))
                    sn['snr_at_max_epoch_%s' % filt] = sn['snr_%s' % filt][max_mag_idx]
                else:
                    sn['max_epoch_%s' % filt] = []
                    max_mag_idx = []
                    sn['snr_at_max_epoch_%s' % filt] = []

            else:
                sn['fluxcal_%s' % filt] = []
                sn['fluxcalerr_%s' % filt] = []
                #sn['maxflux_%s' % filt] = []
                #sn['maxfluxerr_%s' % filt] = []

            del sn[filt]
        sn.update(sn['header'])
        del sn['header']

    return pd.DataFrame.from_dict(data, orient='index')
