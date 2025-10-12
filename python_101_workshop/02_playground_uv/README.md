# Set up

```shell
docker build -t uv_training -f Dockerfile  .
docker run -it --entrypoint /bin/bash --volume ./temp/:/code uv_training
```

# Virtual Environment

Why we need them?

Python looks for modules in 3 steps:-

* First, it searches in the current directory.
* If not found then it searches in the directories which are in shell variable PYTHONPATH
* If that also fails python checks the installation-dependent list of directories configured at the time Python is installed

```shell
root@2088323089d8:/code# python
>>> import sys
>>> sys.path
['', '/usr/local/lib/python313.zip', '/usr/local/lib/python3.13', '/usr/local/lib/python3.13/lib-dynload', '/usr/local/lib/python3.13/site-packages']
```

```shell
root@2088323089d8:/code# PYTHONPATH="/code/random_place" python
>>> import sys
>>> sys.path
['', '/code/random_place', '/usr/local/lib/python313.zip', '/usr/local/lib/python3.13', '/usr/local/lib/python3.13/lib-dynload', '/usr/local/lib/python3.13/site-packages']
```

Note: There are build-in modules loaded in memory together with already imported modules (performance optimization). So if you already import the module, and you change the file, you need to restart the python to see the changes (can be tricky in long-running tasks like Python interpreter or Jupyter Notebook).

```python
import sys
import src.common.logger
print(sys.modules)
# -> {... 'src.common.logger': <module 'src.common.logger' from '/code/src/common/logger.py'>}
# add function def print_greeting() to src.common.logger

from src.common.logger import print_greeting
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ImportError: cannot import name 'print_greeting' from 'src.common.logger' (/code/src/common/logger.py)

import importlib
importlib.reload(src.common.logger)
from src.common.logger import print_greeting
```

Here is an example where the Python look for modules when using astral-UV (or any other virtual environment):

### Python Virtual Environment with focus on UV

TLDR: UV is a tool to manage python versions and dependencies. Such tool usually work on the principle of virtual environment. The main work is to update the PYTHONPATH in a smart way to force the python to look for modules in the right place.

```shell
root@2088323089d8:/code# uv run python 
>>> import sys
>>> print(sys.path)
['', '/root/.local/share/uv/python/cpython-3.12.9-linux-aarch64-gnu/lib/python312.zip', '/root/.local/share/uv/python/cpython-3.12.9-linux-aarch64-gnu/lib/python3.12', '/root/.local/share/uv/python/cpython-3.12.9-linux-aarch64-gnu/lib/python3.12/lib-dynload', '/code/.venv/lib/python3.12/site-packages']
```

The most important part for us is `site-packages` where all the libraries are stored. Let's look inside:

```shell
root@a56e5f8ec208:/code# ls /code/.venv/lib/python3.12/site-packages/requests
__init__.py     _internal_utils.py  api.py   certs.py   cookies.py     help.py   models.py    sessions.py      structures.py
__version__.py  adapters.py         auth.py  compat.py  exceptions.py  hooks.py  packages.py  status_codes.py  utils.py
```

How does it possible that the code is there? Look at any *.whl file. To understand let's look on Structure/Packaging of Python code.


### Structure/Packaging

When you want to distribute your work (or when you install it from Pypi) you need to package it. Be aware that most of the Python libraries are not distributed as a single file, but as a package. A package is a collection of Python modules and sub-packages that are organized in a directory hierarchy. It is just cleverly zipped directory.

```shell
python -m zipfile -c my_package.zip my_package/* # should contain the content not the folder
python my_package.zip
```

Another way how to run the code

```shell
python my_package # since we have __main__

# assume it is package/module -> will look at __init__.py load all the other modules inside ...
python -m my_package
```

The package format can be two types: source distributions (.tag.gz), or sdists for short, and binary distributions, commonly called wheels (.whl). Main differences is in compiled code (like C++) where wheels are compiled for specific platform and sdists are not. Wheels are faster to install because they do not require compilation. For python only code the difference is not that important (but for example wheels are meant to contain exactly what is to be installed, and nothing more. In particular, wheels should never include tests and documentation, while sdists commonly do.) Wheels are the preferred format for installing packages, as they are faster and more efficient than source distributions (which require firstly build a wheel).

* https://peps.python.org/pep-0491/#file-name-convention
* https://pypi.org/project/numpy/#files
* https://packaging.python.org/en/latest/overview/ 
* https://peps.python.org/pep-0517/ 

“Egg” is an old package format that has been replaced with the wheel format. It should not be used anymore. Since August 2023, PyPI rejects egg uploads.

Then you have several tools how to package it, distribute it and so on. 

`twine` - Twine is a utility for publishing Python packages on PyPI. (https://pypi.org/project/twine/) - Can be subtitute by `uv publish`

`setuptools` is a powerful Python library designed to facilitate packaging Python projects. It is related to `setup.py`. `setup.py` is a Python script traditionally used for packaging Python projects. It uses the setuptools library to define the metadata and dependencies of the project. Here is an example of a simple setup.py file:

```python
from setuptools import setup, find_packages

setup(
    name='example_package',                     # Name of the package
    version='0.1.0',                           # Package version
    author='Your Name',                         # Author's name
    author_email='your.email@example.com',     # Author's email
    description='A short description of the package',  # Brief description
    long_description=open('README.md').read(), # Detailed description from README file
    long_description_content_type='text/markdown', # Specify the format of the long description
    url='https://github.com/yourusername/example_package', # Package URL
    packages=find_packages(),                   # Automatically find packages in the directory
    classifiers=[                               # Optional classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                   # Specify the Python version requirement
    install_requires=[                          # List of dependencies, can be different from requirements.txt which is used for dev
        'numpy',                                # Example dependency
        'requests',
    ],
    entry_points={                              # Console scripts
        'console_scripts': [
            'example-script=example_package.module:function',  # Define a command-line script
        ],
    },
)
```

`pyproject.toml` is a newer configuration file introduced by PEP 518 and PEP 517. It aims to standardize the way build system requirements are specified and to solve the "chicken and egg" problem of build dependencies. Here is an example of a pyproject.toml file - https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#a-full-example

It is python-standard for packaging and distribution. It is not only for Astral UV, but also for Poetry, setuptools, and other tools... See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ . However some parts are ignored by different tools - some parts are added by different tools and so on. For example:

```text
A notable exception is Poetry, which before version 2.0 (released January 5, 2025) did not use the [project] table, it used the [tool.poetry] table instead. With version 2.0, it supports both. Also, the setuptools build backend supports both the [project] table, and the older format in setup.cfg or setup.py.
```

There are three important parts - [build-system], [project], [tool] - see https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

But we will look at one tool which is build on top of that - Astral UV.

But back to .whl format.

```shell
root@a56e5f8ec208:/code# uv build
Building source distribution...
...
Successfully built dist/code-0.1.0.tar.gz
Successfully built dist/code-0.1.0-py3-none-any.whl

root@a56e5f8ec208:/code# python -m zipfile --extract dist/code-0.1.0-py3-none-any.whl unzipped_folder         
root@a56e5f8ec208:/code# cat unzipped_folder/main.py 
def main():
    print("Hello from code!")


if __name__ == "__main__":
    main()

```

So, it is just "zip" files when working just with Python.

# Astral UV 

Tool written in Rust to manage Python versions and dependencies. It is a replacement for pyenv, pipenv, poetry, and venv. Disadvantage (in comparison to Poetry) is that it is not written in Python (they claim it as advantage because of speed) but it is not developed by broad Python community but more like by one company. Or people from Rust community. It is not a problem "now", but it is good to know (= you cannot say that I did not warm you :) ).

Advantages:
* speed
* combine multiple other libraries into one

Disadvantages:
* written in Rust
* still in development
* they have custom version of Python (there is discussion in Python Online Coffee if that is safe)

# Prerequisites
## Mac
```bash
brew install uv
```
or look at https://docs.astral.sh/uv/getting-started/installation for other option or platforms.

The docker container is using pip.

```shell
pip install uv
```

# Setup new project

uv supports persistent configuration files at both the project- and user-level.

Specifically, uv will search for a pyproject.toml or uv.toml file in the current directory, or in the nearest parent directory. If it is does not found then it is created with default values. (pyproject.toml vs uv.toml - you can omit tool.uv in the header and uv.toml takes precedence)

Be aware of user-level configuration (e.g., ~/.config/uv/uv.toml) and system-level configuration (e.g., /etc/uv/uv.toml)

## "Get it done and get it fast" way
1. Install python version `uv init`. It will take whatever version of Python you have installed. See `pyproject.toml`. It will create `pyproject.toml`, `main.py` , `README.md` and `.python-version` file.
2. Run `uv run python main.py`. It will create `uv.lock` file and `.venv` folder.


## More description-based way
1. Install specific python version `uv python install 3.12 --native-tls`
2. Create virtual enviroment `uv venv`
3. Pin specific version `uv python pin 3.12` (need to change it in `pyproject.toml` as well if already created)
4. Run `uv run python main.py` (or `uv run --env-file .env python`)


## Install Dependencies
* Add index to look for Python packages `export UV_INDEX_URL=` or in pyproject.toml
* Install library `uv add --dev <library>` or `uv add --group documentation <library>`
* Install from file `uv add --requirement requirements.txt`


## Cheatsheet
* `uv run --with requests python main.py` - run with specific library, it does not add it into the dependencies (install it before the run and remove afterwards)
* Similar to `uvx pycowsay hello from uv` which is `uv tool run pycowsay hello from uv`. You can install tool (modify PATH) and then call it without `uv`
* `uv lock` - update the lock file with packages
* `uv sync`- sync will remove dependencies not in `pyproject.toml` (in comparison to `uv lock`)

```shell
uv pip install requests # be aware that it is different from just pip install requests
uv sync
```

* `uv sync --frozen` - it will use the lock file and will not update it
* `uv sync --no-dev` - The dev group is special-cased and synced by default
* `uv sync --only-group documentation` - Additional groups can be included or excluded with the --all-groups, --no-default-groups, --group <name>, --only-group <name>, and --no-group <name> options.
* `uv sync --extra format` - uv does not sync extras by default. Use the --extra option to include an extra.
* `uv sync --extra dev` - if `[project.optional-dependencies] dev = [...`

* `uv pip tree` - show dependency tree or `uv tree`
* `uv pip install -e .` - install current code in editable mode - basically modifying PATH again, can be handy if the project is used somewhere else

```shell
>>> import sys
>>> sys.path
['', '/root/.local/share/uv/python/cpython-3.12.9-linux-aarch64-gnu/lib/python312.zip', '/root/.local/share/uv/python/cpython-3.12.9-linux-aarch64-gnu/lib/python3.12', '/root/.local/share/uv/python/cpython-3.12.9-linux-aarch64-gnu/lib/python3.12/lib-dynload', '/code/.venv/lib/python3.12/site-packages', '__editable__.code-0.1.0.finder.__path_hook__']
>>> import code
```


* `uv build` - build the project
* `uv publish --index XY` - publish the project to the index (need to be set in pyproject.toml)
* `uv add langchain[dev]` - optional dependency groups - https://github.com/langchain-ai/langchain/blob/master/pyproject.toml
* `uv remove langchain[dev]`

# Links

* https://docs.python.org/3/reference/import.html
* https://fastapi.tiangolo.com/virtual-environments/
* https://docs.astral.sh/uv/configuration/environment/
  * https://docs.astral.sh/uv/concepts/projects/dependencies/
* https://www.loopwerk.io/articles/2024/python-poetry-vs-uv/ + https://www.loopwerk.io/articles/2024/python-uv-revisited/ + https://github.com/astral-sh/uv/issues/1474

# Interesting discussion
* https://github.com/astral-sh/uv/issues/3957
* workspeces - https://federico.is/posts/2024/12/18/managing-python-workspaces-with-uv/?_sm_nck=1

# Build backends

While setuptools has been the de facto standard for Python packaging for many years, there are several reasons why new build backends like Hatchling have emerged:
* Complexity and Usability: Setuptools can be complex and often requires extensive configuration, which can be daunting for new users. Many developers find that the default settings of setuptools are not optimal for their needs, leading to a steep learning curve. Hatchling addresses this by providing "better defaults" that are more user-friendly and require less configuration effort.
* Reproducibility: One of the significant limitations of setuptools is that it does not guarantee reproducible builds for source distributions. This can lead to inconsistencies when packages are built in different environments. Hatchling, on the other hand, is designed to build reproducible wheels and source distributions by default, which is crucial for maintaining consistent environments across different setups.
* Modern Features: Setuptools has deprecated several features over time and is not fully aligned with modern Python packaging standards. For example, it has deprecated direct invocations of setup.py, which can lead to compatibility issues in the future. Hatchling supports modern configurations using pyproject.toml, which is now the recommended way to define project metadata and dependencies.
* Extensibility and Plugin Support: Hatchling is built with extensibility in mind, allowing developers to create plugins to enhance its functionality. This flexibility can be beneficial for projects that require specific build steps or customizations that are not easily achievable with setuptools.

* https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html?ref=sarahglasmacher.com#package-tool-features-table


Commands
```python
import os
os.path.abspath(os.path.curdir)
```