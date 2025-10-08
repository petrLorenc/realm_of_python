# TLDR

Pyenv + Poetry way (I like this more)
```
# install pyenv

# In project folder
pyenv install 3.10.5
pyenv local 3.10.5

# install poetry

# Set Python dependencies with Poetry
poetry config virtualenvs.prefer-active-python true
poetry config virtualenvs.in-project true
poetry install --no-root # this will create the env automatically
eval $(poetry env activate)
```

UV way (more and more popular)
```shell
# install uv - https://docs.astral.sh/uv/getting-started/installation/
wget -qO- https://astral.sh/uv/install.sh | sh
# or
brew install uv


# Set Python dependencies with UV
uv python install 3.12.3
uv venv --python 3.10.5
# not recommended
uv pip install ".[dev]"
# this is better way
uv sync --extra dev 

```
More about `pyproject.toml` - https://realpython.com/python-pyproject-toml/.

Be aware that `pyproject.toml` is not the same for poetry/uv - https://stackoverflow.com/questions/79118841/how-to-migrate-from-poetry-to-uv-package-manager .

# Background

When you want to use anything in your device, you need to have executable to do so. Python is not an exception. When you install Python, you get the Python executable. But what if you want to use a specific version of Python or a specific version of a package? This is where virtual environments come in. If you install Python then it is put inside your PATH (there are many directories which are not related to Python).

```shell
echo "${PATH}"
whereis python # which python
```

Because there is an sequential order when you look for some executable then if you prepend another directory to the PATH where the Python executable is then you will use the Python from that directory. This is how virtual environments work. They prepend the directory where the Python executable is to the PATH. This is why you can have multiple virtual environments with different Python versions or different packages.

```shell
python -m venv my_venv
source my_venv/bin/activate
echo "${PATH}"
whereis python # which python
```

Of course there are many ways how to do this simple step more complicated (but beneficial in a long run). One of the ways is to use dependency management tool like `pipenv` or `poetry`. These tools are not only for managing dependencies but also for managing virtual environments. They are more user friendly and have more features than the built-in `venv` module. There is also `conda` which is a package manager and environment manager. It is more complex than `pipenv` or `poetry` but it is also more powerful. It is used mainly for data science and machine learning (the complexity is similar to `brew`).

Key terminology:
 * requirements.txt - a file that contains the dependencies of a project

## Pyenv

Pyenv is a tool for managing multiple versions of Python. It allows you to install different versions of Python and switch between them. It is a tool that is recommended for developers who need to work with different versions of Python. It is a tool that is more user friendly than `brew` and has more features. It is also more modern and has a better design. It is a tool that is recommended for new projects. Recommended by Poetry - https://python-poetry.org/docs/managing-environments/ . 

### What pyenv does...
* Lets you change the global Python version on a per-user basis.
* Provides support for per-project Python versions.
* Allows you to override the Python version with an environment variable.
* Searches for commands from multiple versions of Python at a time. This may be helpful to test across Python versions with tox.
### In contrast with pythonbrew and pythonz, pyenv does not...
* Depend on Python itself. pyenv was made from pure shell scripts. There is no bootstrap problem of Python.
* Need to be loaded into your shell. Instead, pyenv's shim approach works by adding a directory to your PATH.
* Manage virtualenv. Of course, you can create virtualenv yourself, or pyenv-virtualenv to automate the process.


```shell
pyenv versions
pyenv install 3.10.5




## Poetry

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. It also allows you to create a virtual environment for your project. It is a tool that is more user friendly than `pipenv` and has more features. It is also more modern and has a better design. It is a tool that is recommended for new projects.

```shell
poetry new my_project # create a new project
poetry init # create a new project iteratively 

cd my_project
poetry add requests
poetry install

poetry env info
poetry run python -m my_project
deactivate
```

Key commands:
  * `poetry new my_project` - create a new project
  * `poetry add requests` - add a dependency
  * `poetry install` - install dependencies
  * `poetry run python -m my_project` - run a script
  * `poetry shell` - start a shell in the virtual environment
  * `poetry build` - build a package
  * `poetry publish` - publish a package



### Help (poetry)

```text
Poetry (version 2.0.1)

Usage:
  command [options] [arguments]

Options:
  -h, --help                 Display help for the given command. When no command is given display help for the list command.
  -q, --quiet                Do not output any message.
  -V, --version              Display this application version.
      --ansi                 Force ANSI output.
      --no-ansi              Disable ANSI output.
  -n, --no-interaction       Do not ask any interactive question.
      --no-plugins           Disables plugins.
      --no-cache             Disables Poetry source caches.
  -P, --project=PROJECT      Specify another path as the project root. All command-line arguments will be resolved relative to the current working directory.
  -C, --directory=DIRECTORY  The working directory for the Poetry command (defaults to the current working directory). All command-line arguments will be resolved relative to the given directory.
  -v|vv|vvv, --verbose       Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

Available commands:
  about              Shows information about Poetry.
  add                Adds a new dependency to pyproject.toml and installs it.
  build              Builds a package, as a tarball and a wheel by default.
  check              Validates the content of the pyproject.toml file and its consistency with the poetry.lock file.
  config             Manages configuration settings.
  help               Displays help for a command.
  init               Creates a basic pyproject.toml file in the current directory.
  install            Installs the project dependencies.
  list               Lists commands.
  lock               Locks the project dependencies.
  new                Creates a new Python project at <path>.
  publish            Publishes a package to a remote repository.
  remove             Removes a package from the project dependencies.
  run                Runs a command in the appropriate environment.
  search             Searches for packages on remote repositories.
  show               Shows information about packages.
  sync               Update the project's environment according to the lockfile.
  update             Update the dependencies as according to the pyproject.toml file.
  version            Shows the version of the project or bumps it when a valid bump rule is provided.

 cache
  cache clear        Clears a Poetry cache by name.
  cache list         List Poetry's caches.

 debug
  debug info         Shows debug information.
  debug resolve      Debugs dependency resolution.

 env
  env activate       Print the command to activate a virtual environment.
  env info           Displays information about the current environment.
  env list           Lists all virtualenvs associated with the current project.
  env remove         Remove virtual environments associated with the project.
  env use            Activates or creates a new virtualenv for the current project.

 self
  self add           Add additional packages to Poetry's runtime environment.
  self install       Install locked packages (incl. addons) required by this Poetry installation.
  self lock          Lock the Poetry installation's system requirements.
  self remove        Remove additional packages from Poetry's runtime environment.
  self show          Show packages from Poetry's runtime environment.
  self show plugins  Shows information about the currently installed plugins.
  self sync          Sync Poetry's own environment according to the locked packages (incl. addons) required by this Poetry installation.
  self update        Updates Poetry to the latest version.

 source
  source add         Add source configuration for project.
  source remove      Remove source configured for the project.
  source show        Show information about sources configured for the project.
```

## Help (uv)

```text
uv --help             
An extremely fast Python package manager.

Usage: uv [OPTIONS] <COMMAND>

Commands:
  run      Run a command or script
  init     Create a new project
  add      Add dependencies to the project
  remove   Remove dependencies from the project
  sync     Update the project's environment
  lock     Update the project's lockfile
  export   Export the project's lockfile to an alternate format
  tree     Display the project's dependency tree
  tool     Run and install commands provided by Python packages
  python   Manage Python versions and installations
  pip      Manage Python packages with a pip-compatible interface
  venv     Create a virtual environment
  build    Build Python packages into source distributions and wheels
  publish  Upload distributions to an index
  cache    Manage uv's cache
  self     Manage the uv executable
  version  Display uv's version
  help     Display documentation for a command

Cache options:
  -n, --no-cache               Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation [env: UV_NO_CACHE=]
      --cache-dir <CACHE_DIR>  Path to the cache directory [env: UV_CACHE_DIR=]

Python options:
      --managed-python       Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
      --no-managed-python    Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
      --no-python-downloads  Disable automatic downloads of Python. [env: "UV_PYTHON_DOWNLOADS=never"]

Global options:
  -q, --quiet                                      Do not print any output
  -v, --verbose...                                 Use verbose output
      --color <COLOR_CHOICE>                       Control the use of color in output [possible values: auto, always, never]
      --native-tls                                 Whether to load TLS certificates from the platform's native certificate store [env: UV_NATIVE_TLS=]
      --offline                                    Disable network access [env: UV_OFFLINE=]
      --allow-insecure-host <ALLOW_INSECURE_HOST>  Allow insecure connections to a host [env: UV_INSECURE_HOST=]
      --no-progress                                Hide all progress outputs [env: UV_NO_PROGRESS=]
      --directory <DIRECTORY>                      Change to the given directory prior to running the command
      --project <PROJECT>                          Run the command within the given project directory
      --config-file <CONFIG_FILE>                  The path to a `uv.toml` file to use for configuration [env: UV_CONFIG_FILE=]
      --no-config                                  Avoid discovering configuration files (`pyproject.toml`, `uv.toml`) [env: UV_NO_CONFIG=]
  -h, --help                                       Display the concise help for this command
  -V, --version                                    Display the uv version

```


### Notes (uv)
https://www.loopwerk.io/articles/2024/python-poetry-vs-uv/


https://github.com/astral-sh/uv/issues/6443
```text
[tool.setuptools.packages.find]
where = []
```

https://github.com/astral-sh/uv/issues/1474
```shell
uv python install 3.11          
error: Failed to install cpython-3.11.11-macos-aarch64-none
  Caused by: Failed to download https://github.com/astral-sh/python-build-standalone/releases/download/20250212/cpython-3.11.11%2B20250212-aarch64-apple-darwin-install_only_stripped.tar.gz
  Caused by: Request failed after 3 retries
  Caused by: error sending request for url (https://objects.githubusercontent.com/github-production-release-asset-2e65be/162334160/ee46148b-e976-46be-b949-b7c3a4493cad?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250320%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250320T120559Z&X-Amz-Expires=300&X-Amz-Signature=53b1c321ac6b957cf4e2bde88f515b2df475fadf9d9b5f4715f074939cd96af9&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Dcpython-3.11.11%2B20250212-aarch64-apple-darwin-install_only_stripped.tar.gz&response-content-type=application%2Foctet-stream)
  Caused by: client error (Connect)
  Caused by: invalid peer certificate: UnknownIssuer

# https://docs.astral.sh/uv/configuration/authentication/#custom-ca-certificates
uv python install 3.11 --allow-insecure-host github.com
# or
uv python install 3.11 --native-tls
```

# General notes

https://stackoverflow.com/questions/122327/how-do-i-find-the-location-of-my-python-site-packages-directory/
```shell
python -m site

```