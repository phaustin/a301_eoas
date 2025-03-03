(week8:install_part1)=
# Python packages Part 1 

- Download `install_part1.ipynb` and `requirements.txt` from 
[the week8 folder](https://drive.google.com/drive/folders/1-D6y9MlE8LZRLZg-qRCxPZSgar8kGjBT?usp=drive_links)

- Obligatory [xkcd cartoon](https://xkcd.com/1987/) from around 2017.

## Introduction

This notebook goes over how to install a single python file, like 
[a301_lib.py](https://github.com/phaustin/a301_lib/blob/main/src/a301_lib.py) so it can be imported into the a301 python environment.  The general task of creating, selecting and installing files
is called "package management", and programs that do that are called "package managers".  None of this will be on the final exam, but if you are planning to work with python in the future, all of this should be on your to-learn list at some point relatively soon.

Python packaging is especially complicated, because python has an extensive history (python 1.0 was released in January 1994) that predates any formal way of distributing code.  Python grew up along with the internet, and pioneered many of the ways that modern programming languages install libraries.  That process also meant that there were many competing experiments and dead ends, and a semi-standardized way of packaging libraries has only evolved in the last 5 years or so.  

Many modern languages that were created after python learned from python's successes and failures, and designed a single installation manager from early in the language's evolution (pkg for Julia, cargo for Rust, npm for javascript, etc.)  Python instead has about 6 package managers that can all use the same configuration files but do the basic process of package and environment management slightly differently.  

Python also is different in that
there are two fundamentally different ways of approaching packaging, via the official python repository ([pypi.org](https://pypi.org)) or via conda and [conda-forge.org](https://conda-forge.org).  This notebook only considers creating a package that is
compatible with pypi.org.  A pypi package can also be wrapped as a conda package, but that topic
is out of scope for A301.

## Where to start

There are an excellent set of tutorials developed by the [pyopenscience.org](https://www.pyopensci.org/) and hosted as the [python packaging guide](https://www.pyopensci.org/python-package-guide/).  Their examples use a fairly new
packaging tool called [hatch](https://hatch.pypa.io/latest/).  The a301_lib package instead uses
the oldest python installation program called [setuptools](https://setuptools.pypa.io/en/latest/userguide/) but for this simple example there
is no real difference between the two approaches.

- Step 1:  read [why create a python package](https://www.pyopensci.org/python-package-guide/tutorials/intro.html#why-create-a-python-package)

- Step 2: read [python packaging for scientists](https://www.pyopensci.org/python-package-guide/#python-packaging-for-scientists)

- Step 3: in class walk through of the a301_lib [pyproject.toml](https://github.com/phaustin/a301_lib/blob/main/pyproject.toml)

- Step 4:  how to use the library

  - install with [pip](https://pip.pypa.io/en/stable/)
  
    ```python
    pip install git+https://github.com/phaustin/a301_lib
    ```

  - alternatively, download the [requirements.txt](https://github.com/phaustin/a301_lib/blob/main/requirements.txt) file from [the week8 folder](https://drive.google.com/drive/folders/1-D6y9MlE8LZRLZg-qRCxPZSgar8kGjBT?usp=drive_links) and do:
    
    ```python
    pip install -r requirements.txt
    ```
    
- Step 5: test the installation

  - the following should print out the path to `a301_lib.py` inside your
    miniconda install
    
    ```python
    python -c 'import a301_lib;print(a301_lib.__file__)'
    ```

  - do `conda list` in the terminal and you should see this line:
    ```python
    a301-lib                  0.1                      pypi_0    pypi
    ```
    

```python

```
