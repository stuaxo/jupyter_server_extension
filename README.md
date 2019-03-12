# jupyter_server_extension

Launch [Jupyter server]() extensions as Jupyter applications. 

This is an **experimental** library for making applications out of Jupyter server extensions. 

## How to write an extension

The following describes the pattern for writing a jupyter server extension that also works as a standalone application.

1. Subclass the `JupyterServerExtensionApp`. 
```python
from jupyter_server_extension.application import JupyterServerExtensionApp

class MyExtensionApp(JupyterServerExtensionApp):
    name = "my_extension"

    load_jupyter_server_extension = staticmethod(load_jupyter_server_extension)
    static_file_path = Unicode("/path/to/static/dir/")


    # Traits that will be loaded by Jupyter's config system.
    trait1 = Unicode("trait1").tag(config=True)
    trait2 = Unicode("trait2").tag(config=True)
```
2. Subclass the `JupyterExtensionHandler` to handler API requests. This handler points the `static_url` to namespaced endpoints under the `static` url pattern.  
```python
from jupyter_server_extension.handler import JupyterExtensionHandler

class MyExtensionHandler(JupyterExtensionHandler):

    def get(self):
        self.render_template("index.html")

```
3. Write a `load_jupyter_server_extension` function. The first thing you should do in this function is load your extensions application.

```python
def load_jupyter_server_extension(serverapp):
    # Load the configuration file.
    extension = MyExtension()
    extension.load_config_file()

    webapp = serverapp.web_app

    # Add a handler for serving static files.
    handlers = []
    handlers.append("/my_extension", MyExtensionHandler)
    handlers.append(
        (r"/static/my_extension/(.*)", StaticFileHandler, {"path": extension.static_file_path})
    )

    # Add handlers to jupyter web application.
    webapp.add_handlers(".*$", handlers)
```