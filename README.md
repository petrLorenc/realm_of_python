# Realm of Python

This repository is a collection of Python code snippets, examples, and best practices. It is part of a larger effort to provide hands-on experience with different aspects of Python. It does not aim to replace comprehensive resources; rather, it provides a quick reference for some common problems and solutions. It can also be used as presentation material in some cases.

It was partly used as supporting material for various presentations and workshops I have given since 2023. The topics covered by this repository include:

## Bigger session
* [3x3h Python 101 workshop (03/25)](./python_workshop/)
* [Astral UV - how to use it properly (02/25)](./uv-playground/)
* [Python typing - cheatsheet and some edge cases (08/25)](./typing/)
* [Reimplementation of Gradient Descent (based on Andrej Karpathy's explanation) (06/25)](./pytorch_neural_network/)
* [Reinplemntation of Dependency Injection (05/25)](./own_dependency_injection/) - Inspired by [Python DI library](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)


## Shorter session
* [Process X Thread X Asyncio (waiting for no-GIL) (01/25)](./asynchronous_code/)
* [Dunder methods](./dunder_methods/)
* [Edge cases](./hall_of_fame/)
* [Testing](./tests_code/)

## Badges

I created a system of badges to encourage people to share about different technologies — each badge is a generated image that humorously represents the content of a presentation. Here are examples of badges I made for my presentations:

**Explanation of gradients (how PyTorch works internally):**

![Gradient](imgs/gradient.png)

**How to use Astral UV properly:**
  
![How to use UV](imgs/uv.png)

## How to prepare env

```shell
# be aware of `poetry config --list`
# be aware of virtualenvs.in-project

poetry install --no-root
```

I would advice to use UV from 02/2025. See [uv-playground](./uv-playground/) folder.

```
uv sync
```
