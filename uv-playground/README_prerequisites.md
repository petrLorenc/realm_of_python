# PYTHONPATH is all you need ... to import anything.

Introduction to "importing" machinery behind Python `import` statement.

# Playground set up

```shell
docker build -t uv_training -f Dockerfile  .
docker run -it --rm uv_training # start from scratch and remove the container after exit
```

# Virtual Environment

Why we need them?

Python looks for modules (module is any .py file) in 3 steps:-

* (1) First, it searches in the current directory.
* (2) If not found then it searches in the directories which are in shell variable PYTHONPATH
* (3) If that also fails python checks the installation-dependent list of directories configured at the time Python is installed

```shell
root@2088323089d8:/code# python -c "import sys; print(sys.path)"
['', '/usr/local/lib/python313.zip', '/usr/local/lib/python3.13', '/usr/local/lib/python3.13/lib-dynload', '/usr/local/lib/python3.13/site-packages']
# ^1                                        ^3 ...
```

```shell
root@2088323089d8:/code# PYTHONPATH="/code/random_place" python -c "import sys; print(sys.path)"
['', '/code/random_place', '/usr/local/lib/python313.zip', '/usr/local/lib/python3.13', '/usr/local/lib/python3.13/lib-dynload', '/usr/local/lib/python3.13/site-packages']
# ^1         ^2                      ^3 ...
```

Note: There are build-in modules loaded in memory together with already imported modules (performance optimization). 
So if you already import the module, and you change the file, you need to restart the python to see the changes 
(can be tricky in long-running tasks like Python interpreter or Jupyter Notebook).

Note about Note: When modules appear in sys.modules, they're loaded into memory. But to use them, you still need to explicitly import them into your current namespace

```shell
root@2088323089d8:/code# python -c "import sys; print(sys.modules.keys())"
dict_keys(['sys', 'builtins', '_frozen_importlib', '_imp', '_thread', '_warnings', '_weakref', '_io', 'marshal', 'posix', '_frozen_importlib_external', 'time', 'zipimport', '_codecs', 'codecs', 'encodings.aliases', 'encodings', 'encodings.utf_8', '_signal', '_abc', 'abc', 'io', '__main__', '_stat', 'stat', '_collections_abc', 'errno', 'genericpath', 'posixpath', 'os.path', 'os', '_sitebuiltins', 'site', 'linecache'])
```

Example where reload is needed:

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

TLDR: UV is a tool to manage python versions and dependencies. Such tool usually work on the principle of virtual environment. 
The main work is to update the PYTHONPATH (paths in general) in a smart way to force the python to look for modules in the right place.

```shell
root@09cbf8679840:/clean_workspace# uv run python -c "import sys; print(sys.path)"
['', '/usr/local/lib/python313.zip', '/usr/local/lib/python3.13', '/usr/local/lib/python3.13/lib-dynload', '/usr/local/lib/python3.13/site-packages']
#                                                                                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
root@09cbf8679840:/clean_workspace# uv init
root@09cbf8679840:/clean_workspace# uv run python -c "import sys; print(sys.path)"
# last item
['', '/usr/local/lib/python313.zip', '/usr/local/lib/python3.13', '/usr/local/lib/python3.13/lib-dynload', '/clean_workspace/.venv/lib/python3.13/site-packages']
#                                                                                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

The most important part for us is `site-packages` where all the libraries are stored. Let's look inside:

```shell
root@09cbf8679840:/clean_workspace# ls /clean_workspace/.venv/lib/python3.13/site-packages/ 
__pycache__  _virtualenv.pth  _virtualenv.py
root@09cbf8679840:/clean_workspace# uv add requests
root@09cbf8679840:/clean_workspace# ls /clean_workspace/.venv/lib/python3.13/site-packages/ 
__pycache__      _virtualenv.py  certifi-2025.4.26.dist-info  charset_normalizer-3.4.2.dist-info  idna-3.10.dist-info  requests-2.32.3.dist-info  urllib3-2.4.0.dist-info
_virtualenv.pth  certifi         charset_normalizer           idna                                requests             urllib3

```

### Structure/Packaging

When you want to distribute your work (or when you install it from Pypi) you need to package it. 
Be aware that most of the Python libraries are not distributed as a single file, but as a package. 
A package is a collection of Python modules and sub-packages that are organized in a directory hierarchy. 

```shell
root@09cbf8679840:/clean_workspace# uv init --package example-pkg
root@09cbf8679840:/clean_workspace# cd example-pkg
root@09cbf8679840:/clean_workspace/example-pkg# find | sed 's|[^/]*/|- |g'
.
- pyproject.toml
- README.md
- src
- - example_pkg
- - - __init__.py

```

How is it distributed? Through different artifactory resositories.
We can extract it with `zipfile` module (or any other zip tool) to see the content.

```shell
uv run python -m zipfile --extract flake8-7.2.0-py2.py3-none-any.whl unzipped_folder
```

So, it is just "cleverly" zipped directory. We can create our own package in a similar way:

```shell
root@09cbf8679840:/clean_workspace/example-pkg# echo "def foo(): print('hello')" >> src/example_pkg/my_code.py
root@09cbf8679840:/clean_workspace/example-pkg# python -m zipfile -c my_package.zip src/* # should contain the content not the folder
root@09cbf8679840:/clean_workspace/example-pkg# python -c "import sys; sys.path.insert(0, '/clean_workspace/example-pkg/my_package.zip'); from example_pkg.my_code import foo; foo()"
hello

```

If we want to run it directly, we would need some "entry point" - a function that will be called when the package is executed.
```shell
root@09cbf8679840:/clean_workspace/example-pkg# echo "print('I am running')" >> src/example_pkg/__main__.py
# to make it work we need to be inside of the package (__main__.py need to be in root of zipped file)
root@09cbf8679840:/clean_workspace/example-pkg# cd src/example_pkg/ && python -m zipfile -c /clean_workspace/my_package.zip . && cd /clean_workspace
root@04b998c917c5:/clean_workspace# python my_package.zip 
I am running

```

The package format can be two types: source distributions (.tag.gz), or sdists for short, and binary distributions, commonly called wheels (.whl).
Main differences is in compiled code (like C++) where wheels are compiled for specific platform and sdists are not.
Wheels are faster to install because they do not require compilation. For python only code the difference is not that important 
(but for example wheels are meant to contain exactly what is to be installed, and nothing more. 
In particular, wheels should never include tests and documentation, while sdists commonly do.) 
Wheels are the preferred format for installing packages, as they are faster and more efficient than source distributions (which require firstly build a wheel).

* https://peps.python.org/pep-0491/#file-name-convention
* https://pypi.org/project/numpy/#files
* https://packaging.python.org/en/latest/overview/ 
* https://peps.python.org/pep-0517/ 

“Egg” is an old package format that has been replaced with the wheel format. It should not be used anymore. Since August 2023, PyPI rejects egg uploads.

Then you have several tools how to package it, distribute it and so on. 

`twine` - Twine is a utility for publishing Python packages on PyPI. (https://pypi.org/project/twine/) - Can be subtitute by `uv publish`

`setuptools` is a powerful Python library designed to facilitate packaging Python projects. 
It is related to `setup.py`. `setup.py` is a Python script traditionally used for packaging Python projects. 
It uses the setuptools library to define the metadata and dependencies of the project. 

Here is an example of a simple setup.py file:

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

`pyproject.toml` is a newer configuration file introduced by PEP 518 and PEP 517 (will be discussed in main part). 
It aims to standardize the way build system requirements are specified and to solve the "chicken and egg" problem of build dependencies. 
Here is an example of a pyproject.toml file - https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#a-full-example

It is python-standard for packaging and distribution. It is not only for Astral UV, but also for Poetry, setuptools, and other tools... 
See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ . However some parts are ignored by different tools - 
some parts are added by different tools and so on. For example, a snippet of the documentation from Poetry:

```text
A notable exception is Poetry, which before version 2.0 (released January 5, 2025) did not use the [project] table, it used the [tool.poetry] table instead.
 With version 2.0, it supports both. Also, the setuptools build backend supports both the [project] table, and the older format in setup.cfg or setup.py.
```

There are three important parts - [build-system], [project], [tool] - see https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

But we will look at one tool which is build on top of that - Astral UV.

But back to .whl format.

```shell
root@b3c14d63d619:/clean_workspace/example-pkg# uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/example_pkg-0.1.0.tar.gz
Successfully built dist/example_pkg-0.1.0-py3-none-any.whl


root@b3c14d63d619:/clean_workspace/example-pkg# python -m zipfile --extract dist/example_pkg-0.1.0-py3-none-any.whl unzipped_folder
root@b3c14d63d619:/clean_workspace/example-pkg# cd unzipped_folder/ && find | sed 's|[^/]*/|- |g'
.
- example_pkg
- - __main__.py
- - __init__.py
- - main.py
- - my_package.zip
- example_pkg-0.1.0.dist-info
- - entry_points.txt
- - WHEEL
- - METADATA
- - RECORD

root@b3c14d63d619:/clean_workspace/example-pkg# mkdir some_folder
root@b3c14d63d619:/clean_workspace/example-pkg# tar -xzf dist/example_pkg-0.1.0.tar.gz -C some_folder
root@b3c14d63d619:/clean_workspace/example-pkg# cd some_folder/ && find | sed 's|[^/]*/|- |g'
.
- example_pkg-0.1.0
- - pyproject.toml
- - PKG-INFO
- - README.md
- - .python-version
- - src
- - - example_pkg
- - - - __main__.py
- - - - __init__.py
- - - - main.py
- - - - my_package.zip
- - my_package.zip

```

So, `build` is making just "zip" files when working just with Python.
