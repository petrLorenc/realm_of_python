# Multi-package workspace

This setup is trying to be more classic because you can have multiple project group together by dependencies, but you do not want to share it in one project/location (otherwise use workspaces). You can have the folder with `libs` then another bolder with `projects` and then project from `projects` will use some libs from `libs` as dependency. You have two options:

* specify library/module/dependency by location (directly in dependencies) - you need to use absolute path
* or use `tool.uv.index` to specify the location of the library/module/dependency - you can use relative path

First option look like this:

```text
dependencies = [
    "utils-package @file:///Users/lorencp/PycharmProjects/udps-python-workshop/02_playground_uv/packages/packages/utils-package",
]
```

and the other option look like this:

```text
dependencies = [
    "utils-package",
]

[tool.uv.sources]
utils-package = { path = "../utils-package", editable = true }
```

The key difference is that `editable = true` in the other option. So then with this sequence of commands you will see the difference:

```shell
uv run python
>>> from utils_package.main import main
>>> main()
# change utils_package.main.main
# run again
uv run python
>>> from utils_package.main import main
>>> main()
```

then you will get updated behaviour in the other example but not in the first approach. First approach means that project are not installed in editable mode (it was not the case for UV workspaces where you get always up-to-date code).