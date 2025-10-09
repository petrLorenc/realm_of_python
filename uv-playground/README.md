# UV is all you need ... to get confused

Opinion-based walkthrough of how to use Astral UV properly.

# Astral UV 

Tool written in Rust to manage Python versions and dependencies. It is a replacement for pyenv, pipenv, poetry, and venv. 

Disadvantage (in comparison to Poetry) is that it is not written in Python (they claim it as advantage because of speed) but it is not developed by broad Python community but more like by one company. Or people from Rust community. It is not a problem "now", but it is good to know (= you cannot say that I did not warm you :) ).

Advantages:
* speed
* combine multiple other libraries into one

Disadvantages:
* written in Rust
* still in development (some parts are not implemented yet)
* they have custom version of Python (the question is what was changed)


# Setting

* pyproject.toml or uv.toml (recursive search from ROOT, uv.toml take precedence over pyproject.toml if on the same level)
* ~/.config/uv/uv.toml (only uv.toml format) for user setting (merged with project-level BUT project taking section-level precedence)
* --no-config (disable persistent confing), --config-file (supported uv.toml only and others are ignored)


uv.toml [root of your project]
```
python-downloads = "manual" # won't be using their CPython interpreter - need to use pyenv
default-groups = ["dev", "foo"] # dev is DEFAULT!

[[index]]
name = "XYZ"
url = "ZZZ"
priority = "primary"
```

## Creation of project

Setting the stage (with own python interpreter):

```shell
# Not needed in Docker (we use base image with correct Python version)
pyenv install 3.13.1
pyenv local 3.13.1
uv init --no-managed-python --library/application/package/bare NAME
```

Packages (src layout + entry point/script): https://docs.astral.sh/uv/concepts/projects/init/#packaged-applications
    * CLI interface
Library (src layout + py.typed): https://docs.astral.sh/uv/concepts/projects/init/#libraries
    * empty py.typed is marker that package support type checking  - https://peps.python.org/pep-0561/ 
Application (flat layout + no build-backend): https://docs.astral.sh/uv/concepts/projects/init/#applications
Bare - just "plain" pyproject.toml

Build backend:
    * only if you build library/package
    * setuptools (old but most used), hatchling, poetry ...
        * new build systems usually have only better default values, easier to use, and are faster
    * https://hatch.pypa.io/latest/why/#build-backend (why to use hatchling over setuptools)
        * For legacy reasons, if a build system is not defined, then setuptools.build_meta:__legacy__ is used to build the package.
        * We can set to have empty package ...
    

```shell
>> uv init --no-managed-python --library my_library
>> cd my_library
>> echo '[project]
name = "my-library"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []
[tool.setuptools]
py-modules = []' > pyproject.toml
>> uv build
>> python -m zipfile --extract dist/my_library-0.1.0-py3-none-any.whl unzipped_folder
>> ls -lah unzipped_folder/
```

Let's try to create a library, application, and package:

```
uv init --no-managed-python --library my_library
uv init --no-managed-python --application my_application
uv init --no-managed-python --package my_package
```

## Structure

* pyproject.toml - main part
* uv.lock - This file should be checked into version control, allowing for consistent and reproducible installations across machines.
* pylock.toml - new file format (instead of requirements.txt) to record Python dependencies for installation reproducibility - https://peps.python.org/pep-0751/
    * `uv export -o pylock.toml` + `uv pip sync pylock.toml`

## pyproject.toml

Not specific to UV - https://peps.python.org/pep-0518/ - Specifying Minimum Build System Requirements for Python Projects + https://peps.python.org/pep-0517/ - A build-system independent format for source trees

Three main groups ([Link](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)):

* The [build-system] table is strongly recommended. It allows you to declare which build backend you use and which other dependencies are needed to build your project.
  * Based on https://peps.python.org/pep-0517/ (A build-system independent format for source trees) - kind of interface to build system
* The [project] table is the format that most build backends use to specify your project’s basic metadata, such as the dependencies, your name, etc.

* The [tool] table has tool-specific subtables, e.g., [tool.hatch], [tool.black], [tool.mypy]. We only touch upon this table here because its contents are defined by each tool. Consult the particular tool’s documentation to know what it can contain.

### Tool

```
[[tool.uv.index]]
name = "something"
url = ""
primary = true
```

### Project

* project.dependencies: Published dependencies. (https://peps.python.org/pep-0631/)
    * `uv sync` will include it
* project.optional-dependencies: Published optional dependencies, or "extras". (https://peps.python.org/pep-0631/)
    * `uv sync` will NOT include it
    * `uv sync --all-extra` or `uv sync --extra NAME`
* dependency-groups: Local dependencies for development. (https://peps.python.org/pep-0735/)
    * incluce special group `dev`
    * `uv sync` will include it
    * `uv sync --no-default-groups`

Basic usage:
```
uv add numpy
uv add --group testing pytest
uv add --optional llm openai # -> uv add "my_package[openai]", uv add --extra openai my_package
cd ../my_library
uv add --extra llm ../my_package # PATH - installed non editable
uv sync # all default groups
uv tree
uv run python
```

Confusing example:
```
uv add numpy
uv add --group testing pytest
uv add --group dev requests
uv add --dev loguru

uv run python # ?? import loguru ??
uv run python # ?? import requests ??
uv run python # ?? import pytest ??
uv run python # ?? import numpy ??

uv sync # ?? now
uv run --exact python # ?? now
uv run --frozen python # ?? now
```

#### Editable install
Library and package is not installed as editable by default (to some extend).

```
uv init --no-managed-python --no-workspace --package my_package_one
uv init --no-managed-python --no-workspace --package my_package_two
cd my_package_two
uv add ../my_package_one/

cat << 'EOF' > ../my_package_one/src/my_package_one/my_module.py
def foo():
    return "Hello from my_package_two!"
EOF

uv run python
>>> import my_package_one
>>> my_package_one.foo
AttributeError: module 'my_package_one' has no attribute 'foo'

```

We can use editable install to install package as editable (so we can change it without reinstalling it):

```
uv init --no-managed-python --no-workspace --package my_package_one
uv init --no-managed-python --no-workspace --package my_package_two
cd my_package_two
uv add ../my_package_one/

cat << 'EOF' > ../my_package_one/src/my_package_one/my_module.py
def foo():
    return "Hello from my_package_two!"
EOF

uv run python
>>> from my_package_one.my_module import foo
* No module named 'my_package_one.my_module'

uv add ../my_package_one/ --force-reinstall
uv run python
>>> from my_package_one.my_module import foo

uv add ../my_package_one/ --editable 
cat << 'EOF' > ../my_package_one/src/my_package_one/my_module.py
def another_foo():
    return "Hello from my_package_two!"
EOF
uv run python
>>> from my_package_one.my_module import another_foo

cat << 'EOF' > ../my_package_one/src/my_package_one/my_module.py
def another_foo_hi():
    return "Hello from my_package_two!"
EOF
uv run python
>>> from my_package_one.my_module import another_foo_hi
```

Can be also influenced by build package - https://hatch.pypa.io/1.9/config/build/#dev-mode + https://hatch.pypa.io/1.9/config/environment/overview/#dev-mode

# Notes

* `.env` -> --env-file (can be multiple files)

# Scripts/Tools

## Scripts

A Python script is a file intended for standalone execution, e.g., with python <script>.py. 
Using uv to execute scripts ensures that script dependencies are managed without manually managing environments.


Same as `--no-project` (ignore project dependencies) + `--with LIBRARY --with ANOTHER_LIBRARY`. Can be used with shebang to create executable files. `#!/usr/bin/env -S uv run --script`

```
cat << 'EOF' > example.py

import os
import openai

openai.api_type = "azure"
openai.azure_endpoint = os.getenv("ENDPOINT")
openai.api_version = "2024-10-21"
openai.api_key = os.getenv("API_KEY")

response = openai.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",  # engine needs to also contain model's version (here 2024-07-18)
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information.",
        },
        {"role": "user", "content": "What is an API?"},
    ],
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
)
print(response.choices[0].message.content)
EOF
# if send to someone else
uv add --index "XY" --script example.py 'openai'
uv run --env-file .env example.py
```

## Tools

Tools are Python packages that provide command-line interfaces.

uv includes a dedicated interface for interacting with tools. 
Tools can be invoked without installation using uv tool run, in which case their dependencies are installed in a temporary virtual environment isolated from the current project.

Execution (create venv, run, remove). Installation (create venv, install, run)

* `uvx pycowsay hello from uv` == `uv tool run pycowsay hello from uv`
* `uv tool install pycowsay` -> `pycowsay hello from uv`

# Docker

```
# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```
Or old-school
```
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --no-cache-dir -U uv==0.6.7 pip==24.3
```

# Workspaces

* Dependencies between workspace members are editable.

```
uv init --no-managed-python --package my_root
cd my_root/src
uv init --no-managed-python --package project_a
uv init --no-managed-python --package project_b
cd project_b
uv add project_a
uv add tqdm

uv run --package project_b --exact python
uv run --package project_a --exact python
```