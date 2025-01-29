(pixi_install)=
# pixi install for macos and windows

## Introduction

There has been a lot of recent effort into developing modern installation tools for python.  One result is a conda replacement called pixi, developed with an open source license by a company
called [prefix.dev](https://prefix.dev/).   If you're having issues with a conda environment, there's
a good chance pixi might provide a more reliable alternative.

## Installation

### Macos

- open a terminal and at the prompt type

```
cd ~/repos/a301
```

At the prompt, type:

```
curl -fsSL https://pixi.sh/install.sh | bash
```

which will run the installer.  Open a new terminal and type:

```
pixi --help
```

to test the installation.


### Windows

open a powershell terminal and type:

```
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

which will run the installer.  Open a new terminal and type:

```
pixi --help
```

to test the installation.

## remove the installation

- pixi is just a single file stored in
 
  ```
  ~/.pixi/bin/pixi
  ```

  to uninstall, move `~/.pixi` to the trash

## Creating the default a301 environment

- Download the file [pixi.toml](https://drive.google.com/file/d/1WDzlxmXF5mqMcvgGu8oNE8sKvQNCN3Ru/view?usp=sharing)
- Use finder or explorer to move the files to `~/repos/a301`
- in the terminal, `cd ~/repos/a301`
- at the prompt type

  ```
  pixi update
  ```

  which will install all the python packages in a new folder called at `~/repos/a301/.pixi` and
  write a lock file called `~/repos/a301/pixi.lock` which shows every installed package
    
- Start jupyter by typing

  ```
  pixi run jupyter lab
  ```
  at the prompt
  
