# jupyter_server_extension

Launch [Jupyter server]() extensions as Jupyter applications. 

This is an **experimental** library for making applications out of Jupyter server extensions. 

## How to write an extension

The following describes the pattern for writing a jupyter server extension that also works as a standalone application.

1. Subclass the `ExtensionHandler` to handler API requests. This handler points the `static_url` to namespaced endpoints under the `static` url pattern.  

```python
from jupyter_server_extension.handler import JupyterExtensionHandler

class MyExtensionHandler(ExtensionHandler):

    def get(self):
        self.render_template("index.html")

```

2. Subclass the `ExtensionApp` and add handlers.

```python
from traitlets import Unicode
from jupyter_server_extension.application import ExtensionApp

class MyExtensionApp(ExtensionApp):

    name = Unicode("my_extension")
    static_file_path = Unicode("/path/to/static/dir/")

        
    def initialize_handlers(self):
        self.handlers = []
        self.handlers.append(
            (r'/myextension', MyExtensionHandler)
        )

# `launch_instance` method offers an entry point to start the server and application. 
main = MyExtensionApp.launch_instance

# `load_jupyter_server_extension` method allows extension to be appended to already running server. 
load_jupyter_server_extension = MyExtensionApp.load_jupyter_server_extension
```

## What is this library? 

