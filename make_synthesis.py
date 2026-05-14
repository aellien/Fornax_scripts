##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 23/06/2025

@author: aellien
"""
import sys
import dawis as d
import glob as glob
import os
import numpy as np
import pyregion as pyr
import random
import gc
import h5py
import pandas as pd
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.io import fits
from astropy.convolution import convolve
from astropy.coordinates import SkyCoord
from astropy.visualization import *
from astropy.table import Table
from astropy.wcs import WCS
from scipy.stats import kurtosis
from datetime import datetime
from photutils.segmentation import SourceFinder, SourceCatalog, detect_sources, make_2dgaussian_kernel
from photutils.background import Background2D, MedianBackground

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def synthesis_large_sources( oim, header, nfwp, lvl_sep, xs, ys, kurt_filt = True, write_fits = True ):

    # Empty arrays for models
    recim = np.zeros( (xs, ys) )
    xc = xs / 2.
    yc = ys / 2.

    # List of files to read
    opath = nfwp + '*ol.it*.hdf5'
    opathl = glob.glob(opath)
    opathl.sort()
    print(opath)

    # Iterate over iteration files
    for i, op in enumerate(opathl):
        print('Reading iteration %d' %(i), end ='\r')
        with h5py.File(op, "r") as f1:

            # Empty lists for selected atoms within this iteration
            gc.collect()

            # Iterate over objects
            for o in f1.keys():

                # Read data
                x_min, y_min, x_max, y_max = np.copy(f1[o]['bbox'][()])
                image = np.copy(f1[o]['image'][()])
                det_err_image = np.copy(f1[o]['det_err_image'][()])
                lvlo = np.copy(f1[o]['level'][()])
                wr = np.copy(f1[o]['norm_wr'][()])
                '''
                # Compute a few quantities
                sx = x_max - x_min
                sy = y_max - y_min
                try:
                    m = detect_sources(image, threshold = 0., npixels=1)
                    c = SourceCatalog(image, m)
                    xco = int(c.centroid_quad[0][1] + x_min)
                    yco = int(c.centroid_quad[0][0] + y_min)
                except:
                    xco = int(sx / 2. + x_min)
                    yco = int(sy / 2. + y_min)
                '''
                    
                # Filter bad atoms/artifacts
                if kurt_filt == True:
                    k = kurtosis(image.flatten(), fisher=True)
                    if k < 0:
                        gc.collect()
                        continue

                # Add to full reconstructed image of small source
                if (lvlo >= lvl_sep):
                    recim[ x_min : x_max, y_min : y_max ] += image
                    continue
                '''elif (np.isnan(mall[xco, yco])) & (lvlo <= lvl_sep_max):
                    recim[ x_min : x_max, y_min : y_max ] += image
                    continue
                elif (np.isnan(mstar[xco, yco])) & (lvlo > lvl_sep_max):
                    recim[ x_min : x_max, y_min : y_max ] += image
                else:
                    continue'''

    # Write synthesized models to disk
    if write_fits == True:
        
        # LVL SEP
        hdu = fits.PrimaryHDU()
        hdu_oim = fits.ImageHDU(oim, name = 'ORIGINAL', header = header)
        hdu_recim = fits.ImageHDU(recim, name = 'REC.', header = header)
        hdu_res = fits.ImageHDU(oim - recim, name = 'RESIDUALS', header = header)
        hdul = fits.HDUList([ hdu, hdu_oim, hdu_recim, hdu_res ])
        hdul.writeto( nfwp + '.synth.lvl_sep.fits', overwrite = True )
        print('wrote to %s \n'%(nfwp + '.synth.lvl_sep.fits'))
        
    return None

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def replace_none_with_nan(list):
    return [-999. if a is None else a for a in list]
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if __name__ == '__main__':

    # Paths, lists & variables
    path_data = '/n08data/ellien/Euclid_Fornax/data'
    path_wavelets = '/n08data/ellien/Euclid_Fornax/wavelets/out1/'
        
    # Input files
    cutl = 'cutout_VIS_bin4_ext.fits'

    # Cosmology
    H0 = 70.0 # Hubble constant
    Om_M = 0.3 # Matter density
    Om_Lam = 0.7 # Energy density
    
    # spatial scales related
    pix_scale = 0.4 # pixel scale [arcsec/pix]
                
    # wavelet scales related
    lvl_sep = 7 # wavelet scale separation
    lvl_sep_max = 9
    n_levels = 9
    
    # photometry
    ZP_AB  = 30.

    # misc
    kurt_filt = True
    write_fits = True
    
    # cut
    nfp = os.path.join(path_data, cut)
    hdu = fits.open(nfp)
    head = hdu[0].header
    oim = hdu[0].data
    print('Reading %s'%nfp)

    '''
        # mask all sources
        mnfp = nfp[:-4]+'masked.fits'
        mhdu = fits.open(mnfp)
        mall = mhdu[0].data
        print('Reading %s'%mnfp)
        

        # mask bright stars
        mnfp = nfp[:-4]+'mstar.fits'
        if os.path.isfile(mnfp):
            mhdu = fits.open(mnfp)
            mstar = mhdu[0].data
            print('Reading %s'%mnfp)
        else:
            mstar = np.zeros(oim.shape)
    '''
        
    # wavelets
    nfwp = os.path.join(path_wavelets, cut[:-5])
        
    xs, ys = oim.shape
    xc, yc = xs / 2., ys / 2.

    # synthesis
    synthesis_small_sources( im = oim,
                                 header = head, 
                                 nfwp = nfwp, 
                                 lvl_sep = lvl_sep, 
                                 xs = xs, 
                                 ys = ys, 
                                 kurt_filt = kurt_filt,
                                 write_fits = write_fits )
        
