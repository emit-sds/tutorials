# EMIT Python Tutorials

This repository contains several Jupyter notebooks for working with Earth Surface Mineral Dust Source Investigation (EMIT) data products.

To access EMIT Data visit: <https://search.earthdata.nasa.gov/search?fi=EMIT%2BImaging%2BSpectrometer>

## Background  

The EMIT Project delivers space-based measurements of surface mineralogy of the Earth’s arid dust source regions. These measurements are used to initialize the compositional makeup of dust sources in Earth System Models (ESMs). The dust cycle, which describe the generation, lofting, transport, and deposition of mineral dust, plays an important role in ESMs.  Dust composition is presently the largest uncertainty factor in quantifying the magnitude of aerosol direct radiative forcing.  By understanding the composition of mineral dust sources, EMIT aims to constrain the sign and magnitude of dust-related radiative forcing at regional and global scales. During its one-year mission on the International Space Station (ISS), EMIT will make measurements over the sunlit Earth’s dust source regions that fall within ±52° latitude. EMIT will schedule up to five visits (three on average) of each arid target region and only acquisitions not dominated by cloud cover will be downlinked. EMIT-based maps of the relative abundance of source minerals will advance our understanding of the current and future impacts of mineral dust in the Earth system.

The EMIT instrument is a Dyson imaging spectrometer that uses contiguous spectroscopic measurements in the visible to short wave infrared region of the spectrum to resolve absorption features of dust-forming minerals.

The L2A Reflectance Product contains estimated surface reflectance. Surface reflectance is the fraction of incoming solar radiation reflected Earth's surface. Different materials reflect different proportions of radiation based opon their chemical composition, meaning that this information can be used to determine the composition of a target. In this guide you will learn how to plot a layer from the L2A reflectance spatially and look at the spectral curve associated with individual pixels, which can be used to identify targets.

### File Structure  

Inside the `.netcdf` file there are 3 groups, the root group containing reflectance values accross the downtrack, crosstrack, and bands dimensions, the `sensor_band_parameters`  group containing the wavelength of each band center, and the full-width half maximum (FWHM) or bandwidth at half of the maximum amplitude, and the `location` group containing latitude and longitude values of each pixel as well as a geometric lookup table (GLT). The GLT is an orthorectified image that provides relative downtrack and crosstrack reference locations from the raw scene to facilitate fast projection of the dataset.  

### Helpful Links  

[EMIT Website](https://earth.jpl.nasa.gov/emit/)  

[L2A Reflectance User Guide](https://lpdaac.usgs.gov/documents/1569/EMITL2ARFL_User_Guide_v1.pdf)  

[L2A ATBD Documents](https://lpdaac.usgs.gov/documents/1571/EMITL2A_ATBD_v1.pdf)  

### Granules Used

+ <https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20220903T163129_2224611_012/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc>

---

## Notebooks Outline  

---

1. **Exploring EMIT L2A Reflectance Data**
    1.1 Setup  
    1.2 Opening and Understanding File Structure  
    1.3 Plotting Spectra Basics  
    1.4 Geocorrection/Applying GLT  
    1.5 Spatial Plotting (Imagery)  
    1.6 Exploring Spectral and Spatial Plots  

---

## Prerequisites  

---

### 1. Python Environment Setup

This Python Environment will work for all of the tutorials within this repository.

It is recommended to use [Conda](https://conda.io/docs/), an environment manager, to set up a compatible Python environment. Download Conda for your OS [here](https://www.anaconda.com/download/). Once you have Conda installed, follow the instructions below to successfully setup a Python environment on Windows, MacOS, or Linux.  

**Using your preferred command line interface (command prompt, terminal, cmder, etc.) navigate to the repository, then type the following to successfully create a compatible python environment using the included `yml` file. Then launch Jupyter Notebook to get started:**

> `conda env create -f emit_tutorials.yml`

> `conda activate emit_tutorials`

> `jupyter notebook`

**Using your preferred command line interface (command prompt, terminal, cmder, etc.) type the following to successfully create a compatible python environment and launch Jupyter Notebook to get started:**  

> `conda create -n emit_tutorials -c conda-forge python gdal numpy pandas matplotlib xarray rasterio rioxarray geopandas pyproj shapely geoviews cartopy hvplot holoviews netcdf4 jupyter`  

> `conda activate emit_tutorials`  

> `jupyter notebook`  

  TIP: Having trouble activating your environment, or loading specific packages once you have activated your environment? Try the following:
  > `conda update conda`  

If you prefer to not install Conda, the same setup and dependencies can be achieved by using another package manager such as pip.  

[Additional information](https://conda.io/docs/user-guide/tasks/manage-environments.html) on setting up and managing Conda environments.  
**Still having trouble getting a compatible Python environment set up? Contact [LP DAAC User Services](https://lpdaac.usgs.gov/lpdaac-contact-us/).**

### 2. Directory Setup  

This repository requires that you download [this](https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20220903T163129_2224611_012/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc) EMIT scene.

**Place the downloaded file into the `/emit-tutorials/` directory.**

---  

## Data Used/Included in this Repository

---  

The Jupyter notebook, in addition to the Python module used to apply the GLT are included in the repository. The scene used in the notebook can be found [here](https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20220903T163129_2224611_012/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc).  

---

## Contact Info:  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 11-21-2022  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
