from __future__ import annotations

import functools
import typing
import uuid
from typing import (
    Annotated,
    Callable,
    Generic,
    Dict,
    Any,
    Optional,
    Type,
    get_type_hints,
)
from enum import StrEnum


T = typing.TypeVar("T")


class DependencyRegistry:
    """Central repository for managing injectable dependencies."""

    def __init__(self):
        self._dependencies: Dict[str, Callable] = {}
        self._instances: Dict[str, Any] = {}  # For singleton instances

    def register(self, func: Callable, name: Optional[str] = None) -> Callable:
        """Register a dependency provider function."""
        key = name or func.__name__
        self._dependencies[key] = func
        return func

    def get(self, name: str) -> Optional[Callable]:
        """Get a dependency provider by name."""
        return self._dependencies.get(name)

    def get_instance(self, name: str, create_if_missing: bool = True) -> Any:
        """Get or create a singleton instance of a dependency."""
        if name not in self._instances and create_if_missing:
            provider = self.get(name)
            if provider is None:
                raise KeyError(f"No dependency provider registered for: {name}")
            self._instances[name] = provider()
        return self._instances.get(name)

    def list_dependencies(self) -> Dict[str, Callable]:
        """List all registered dependencies."""
        return self._dependencies.copy()

    def clear(self):
        """Clear all registered dependencies and instances."""
        self._dependencies.clear()
        self._instances.clear()

    def __contains__(self, key: str) -> bool:
        return key in self._dependencies


# Create a global registry
registry = DependencyRegistry()


def _infer_dependencies(func: Callable) -> dict[str, Depends]:
    annotations = get_type_hints(func, include_extras=True)
    dependencies = {}
    for name, annotation in annotations.items():
        if hasattr(annotation, "__metadata__"):
            for metadata in annotation.__metadata__:
                if isinstance(metadata, Depends):
                    dependencies[name] = metadata
    return dependencies


class Depends(Generic[T]):
    """Represents a dependency on a function or component."""

    def __init__(self, func_or_name: Callable[..., T] | str):
        self.source = func_or_name
        self._deps = None

    def _get_function(self) -> Callable[..., T]:
        """Get the actual function this dependency refers to."""
        if isinstance(self.source, str):
            # Look up by name in the registry
            func = registry.get(self.source)
            if func is None:
                raise KeyError(f"No dependency registered with name: {self.source}")
            return func
        return self.source

    def _get_deps(self):
        """Lazily resolve dependencies to avoid circular reference issues."""
        if self._deps is None:
            func = self._get_function()
            self._deps = _infer_dependencies(func)
        return self._deps

    def solve(self) -> T:
        """Resolve this dependency and all its dependencies."""
        func = self._get_function()
        deps = self._get_deps()

        solved_deps = {name: dependency.solve() for name, dependency in deps.items()}

        return func(**solved_deps)


class DI_Type(StrEnum):
    injectable = "injectable"
    injector = "injector"


def di(di_type: DI_Type):
    """Dependency injection decorator factory."""

    def inject(func):
        match di_type:
            case DI_Type.injectable:
                # Register the function in the global registry
                registry.register(func)
                return func

            case DI_Type.injector:
                dependencies = _infer_dependencies(func)

                @functools.wraps(func)
                def _wrapper(*args, **kwargs):
                    # Resolve all dependencies
                    solved = {
                        name: dependency.solve()
                        for name, dependency in dependencies.items()
                        if name not in kwargs  # Don't override explicit kwargs
                    }

                    return func(*args, **{**kwargs, **solved})

                return _wrapper

            case _:
                raise ValueError(f"Unknown DI type: {di_type}")

    return inject


# Convenience aliases
inject = di(DI_Type.injector)
injectable = di(DI_Type.injectable)

if __name__ == "__main__":
    # Example with central registry

    # Register dependencies
    @injectable
    def a():
        return 1

    @injectable
    def b():
        return 2

    @injectable
    def c(b: Annotated[int, Depends(b)]):
        return b + 3

    # Using dependencies by reference
    @inject
    def example_by_reference(
        a: Annotated[int, Depends(a)], b: Annotated[int, Depends(b)]
    ):
        return f"Sum of a and b: {a} + {b} = {a + b}"

    # Using dependencies by name
    @inject
    def example_by_name(
        a: Annotated[int, Depends("a")], c: Annotated[int, Depends("c")]
    ):
        return f"Sum of a and b: {a} + {c} = {a + c}"

    print(example_by_reference())
    print(example_by_name())

    # List all registered dependencies
    print("Registered dependencies:", list(registry.list_dependencies().keys()))
