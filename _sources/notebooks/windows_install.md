(windows_install)=
# Windows installation using a conda lock file

If you're having trouble running the landsat notebook from the environment created by environment.yml, try these steps to reproduce exactly the working environment I have in windows.

1. Close all your anaconda terminal windows and in `settings-> add or remove programs` remove miniconda3.

2. Open explorer and go to Home and search for miniconda3.  You should not see a miniconda3 folder in your `c:\Users\username` folder.  If you do see it, remove that folder.

3. Install the latest version of miniconda from [https://www.anaconda.com/download](https://www.anaconda.com/download) (Note that you can skip registration if you want).

4. Check under `add remove programs` to make sure you see `Miniconda3 py312_24.11.1-0`

5. Download my [environment_windows.yml](
https://drive.google.com/file/d/10KLRb80RB8xfq_AMfYdOUrDny5q2bC22/view?usp=sharing) file. Google drive seems to think it's an audio file, but it's just plain text.  You can look at it [here](https://github.com/phaustin/a301_eoas/blob/main/environment_windows.yml).  Note that unlike `environment.yml`, it skips the solver and uses the exact file list from my `a301` environment.

6. Move the `environment_windows.yml` file to your `~/repos/a301` folder, and create a new `a301` environment by opening an anaconda terminal and typing:

```
cd ~/repos/a301
conda env create -n a301 -f environment_windows.yml
conda activate a301
```

7. Start `jupyter lab` and run the `get_landsat_bands.ipynb` notebook.  Note that the new environment includes `earthaccess` etc., so no need go install those. Report any issues on piazza.

