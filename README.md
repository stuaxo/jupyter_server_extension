# jupyter_server_extension

Launch [Jupyter server]() extensions as Jupyter applications. 

This is an **experimental** library for making applications out of Jupyter server extensions. Extensions that 


## How to write an extension

1. Write a `JupyterExtensionApplication`
```python

class MyExtension(JupyterExtensionApplication):



    load_jupyter_server_extension = staticmethod



```

2. Handlers inherit the `JupyterExtensionHandler`. This handler adds a namespace

3. 