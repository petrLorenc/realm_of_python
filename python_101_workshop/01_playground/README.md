# Set up

```
docker build -t syntax_training -f Dockerfile  .
docker run -it -p 9999:9999 syntax_training
```

# Set up with UV

Using Jupyter as a standalone tool
If you ever need ad hoc access to a notebook (i.e., to run a Python snippet interactively), you can start a Jupyter server at any time with uv tool run jupyter lab. This will run a Jupyter server in an isolated environment.

```shell
brew install uv
uv tool run jupyter lab
```

# Links

* https://pythontutor.com/visualize.html
* https://docs.python.org/3/reference/datamodel.html
* https://python-history.blogspot.com/2010/06/method-resolution-order.html