# Breakthrough_Listen_SRT
Useful scripts and information for optimizing the use of turboSETI and plotSETI on Sardinia Radio Telescope datasets for the SETI project.

# First Step: Folder Structure
From `/datax/yyyymmdd/GUPPI` all `0000.fil` should be copied (in order to have a backup) at the path `/datax/users/obs/name_of_the_user/yyyymmdd`.

Once copied, the `.fil` files should be organized into subfolders named accordingly. For example, if you are working on a TESS target you should have something like this:
`/datax/users/obs/simone/20240803/TIC148679712`
Inside the folder, you should have the 6 `.fil` files (3 ONs and 3 OFFs). 

# Second Step: Path corrections
Download `turbo_seti_GC_1.6.py` inside your user folder and create two folders:
`mkdir OUTPUT`
`mkdir OUTPUT_REVERSED` ( the last one is important if you are working on Galactic Center datasets).
Than open the `.py` script and change the following line with your user name:
`BASEDIR = os.path.join("/datax/users/obs/simone", args.date)`
You also may need to change the `OUTPUT_DIR` path.

# Third Step: Run the script
Activate the conda environment `conda activate turboseti`, and then run the following line:
`python turbo_seti_GC_1.6.py yyyymmdd s_value f_value off_value` where `yyyymmdd` is the day/folder you want to analize, `s_value` is the SNR threeshold (10 is suggested), `f_value` sets the filter (you'll need to run the script two times, with f_value=3 and f_value=2), and `off_value` that can be set to `on` if you want to assume that the first `.fil` file is a ON, and `off` if otherwise.
