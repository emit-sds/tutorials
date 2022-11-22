"""
This Module has the functions to apply an EMIT geometry lookup table (GLT) assuming the data has been read into xarray datasets. 

note: Building the xarray dataset output is dependent on the names of variables within the groups
     'sensor_band_parameters' and 'location' as well as the presence of those groups in the dataset. 
     Also, this currently does not work with mask layers (i.e. EMIT_L2A_MASK)

Modified from https://github.com/isofit/isofit/blob/master/.imgspec/apply_glt.py

Author: Erik Bolch, ebolch@contractor.usgs.gov 

Last Updated: 11/16/2022
"""
import netCDF4 as nc
import numpy as np
import math
import pandas as pd
import xarray as xr
from affine import Affine

GLT_NODATA_VALUE = 0
fill_value = -9999

# Function to Calculate the Lat and Lon Vectors/Coordinate Grid
def coord_vects(ds,loc):
    """
    This function calculates the Lat and Lon Coordinate Vectors using the GLT and Metadata from an EMIT dataset read into xarray.
    
    Parameters:
    ds: an xarray.Dataset containing the root variable and metadata of an EMIT dataset
    loc: an xarray.Dataset containing the 'location' group of an EMIT dataset

    Returns:
    lon, lat (numpy.array): longitute and latitude array grid for the dataset

    """
    # Retrieve Geotransform from Metadata
    GT0 = ds.geotransform[0]
    GT1 = ds.geotransform[1]
    GT2 = ds.geotransform[2]
    GT3 = ds.geotransform[3]
    GT4 = ds.geotransform[4]
    GT5 = ds.geotransform[5]
    # Create Array for Lat and Lon and fill
    dim_x = loc.glt_x.shape[1]
    dim_y = loc.glt_x.shape[0]
    lon = np.zeros(dim_x)
    lat = np.zeros(dim_y)
    for x in np.arange(dim_x):
        y=0 # No Rotation
        x_geo = GT0 + x * GT1 + y * GT2
        lon[x] = x_geo
    for y in np.arange(dim_y):
        x=0 # No Rotation
        y_geo = GT3 + x * GT4 + y * GT5
        lat[y] = y_geo
    return lon,lat

# Function to Apply the GLT to a EMIT Dataset
def apply_gltx(filepath):
    """
    This function applies a geometry lookup table to the desired EMIT dataset.

    Parameters:
    filepath: the path to the EMIT dataset (.nc)

    Returns: 
    out_xr: an xarray.Dataset containing the geolocated EMIT dataset and metadata
    """
    ncdf = nc.Dataset(filepath)
    grp_list = list(ncdf.groups.keys())

    ds = xr.open_dataset(filepath)
    loc = xr.open_dataset(filepath, group=grp_list[1])
    wvl = xr.open_dataset(filepath, group=grp_list[0])

    var_list = list(ds.keys())
    
    # Define GLT Dataset
    glt_ds = np.nan_to_num(np.stack([loc['glt_x'].data,loc['glt_y'].data],axis=-1),nan=GLT_NODATA_VALUE).astype(int)

    # Define Rawspace Dataset Variable Values (Typically Reflectance)
    for var in var_list:
        raw_ds = ds[var].data

        # Build Output Dataset
        out_bands = np.arange(raw_ds.shape[-1])
        out_ds = np.zeros((glt_ds.shape[0], glt_ds.shape[1], len(out_bands)), dtype=np.float32) + fill_value
        
        for line in range(glt_ds.shape[0]):
            glt_line = np.squeeze(glt_ds[line,...]).copy()
            valid_glt = np.all(glt_line!=GLT_NODATA_VALUE, axis=-1)
            # Adjust for One based Index
            glt_line[valid_glt, :] = glt_line[valid_glt, :] - 1

            if np.sum(valid_glt) > 0:
                out_ds[line, valid_glt, :] = raw_ds[glt_line[valid_glt, 1][:, None], glt_line[valid_glt, 0][:, None], out_bands[None, :]].copy()

        # Calculate Lat and Lon Vectors
        lon, lat = coord_vects(ds,loc)

        # Create Dictionaries for Output Dataset
        data_vars = {var:(['Latitude','Longitude','bands'], out_ds)} 
        coords = {'Latitude':(['Latitude'],lat), 'Longitude':(['Longitude'],lon), **wvl.variables} # unpack wvl to complete coordinates dictionary

        # Build Xarray Dataset
        out_xr = xr.Dataset(data_vars=data_vars, coords = coords, attrs= ds.attrs)
        
        # Set data_vars array attributes
        out_xr[var].attrs = ds[var].attrs  
    
        # Define Transform and CRS in coordinates of Xarray
        #transform = Affine(out_xr.geotransform[0],out_xr.geotransform[1],out_xr.geotransform[2],out_xr.geotransform[3],out_xr.geotransform[4],out_xr.geotransform[5])
        #out_xr.rio.write_crs(out_xr.spatial_ref,inplace = True)
        #out_xr.rio.write_transform(transform, inplace= True)
    
        # Mask Fill Values
        out_xr = out_xr.where(out_xr[var] != fill_value)
    
    return out_xr

