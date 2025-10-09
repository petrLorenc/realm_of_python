# Multi-package workspace

This setup is a multi-package workspace that contains multiple packages. Each package can be developed and tested independently, but they can also be used together in a single project. Advantage is that each one is editable so no need to refresh the packages after each change. The packages are organized in a single directory structure, and they can be installed using pip.

# Notes

Each package needs to specify build-system (it should be probably the same one - not tested) and specify from what the package is created.

```text
[build-system]
requires = ["hatchling >= 1.26"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/utils_package"]
```

# Links

* https://docs.astral.sh/uv/concepts/projects/workspaces/#workspace-sources
* https://federico.is/posts/2024/12/18/managing-python-workspaces-with-uv/?_sm_nck=1