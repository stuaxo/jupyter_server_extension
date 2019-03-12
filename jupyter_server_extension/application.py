import sys

from traitlets.config.application import catch_config_error
from jupyter_server.serverapp import ServerApp
from jupyter_core.application import JupyterApp


class JupyterServerExtensionApp(JupyterApp):
    """A base class for writing Jupyter server extensions that also
    behave like stand alone Jupyter applications. 

    These applications can be loaded using jupyter_server's 
    extension loading mechanism (and `load_server_extension_function`)
    or launched using Jupyter's command line interface.

    To write an extension application, write a subclass of
    `JupyterServerExtensionApp` and a `load_jupyter_server_extension`
    function. See the example below:

    .. code-block:: python

        class MyExtensionApp(JupyterExtensionApplication):
            name = "my_extension"

            load_jupyter_server_extension = staticmethod(load_jupyter_server_extension)
            static_file_path = Unicode("/path/to/static/dir/")

            # Traits that will be loaded by Jupyter's config system.
            trait1 = Unicode("trait1").tag(config=True)
            trait2 = Unicode("trait2").tag(config=True)


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
    """
    @staticmethod
    def load_jupyter_server_extension(serverapp):
        raise Exception("Must be implemented in a subclass.")

    def initialize_config(self):
        """Load configurations outside of the command line interface."""
        self.load_config_file()

    def initialize_server(self):
        """Create an instance of the jupyter_server ServerApp and initialize."""
        self.serverapp = ServerApp()
        self.serverapp.initialize()
    
    @catch_config_error
    def initialize(self, argv=None):
        """Initialize the server extension using the `load_jupyter_server_extension` function.
        """
        # don't hook up crash handler before parsing command-line
        if argv is None:
            argv = sys.argv[1:]
        if argv:
            subc = self._find_subcommand(argv[0])
            if subc:
                self.argv = argv
                self.subcommand = subc
                return
        self.load_jupyter_server_extension(self.serverapp)
        self.parse_command_line(argv)

    def start(self):
        """Starts the ServerApp first, then launches the extension."""
        self.serverapp.start()
        super(JupyterServerExtensionApp, self).start()

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        """Launch the ServerApp and Server Extension Application. 
        
        Properly orders the steps to initialize and start the server and extension.
        """
        app = cls.instance(**kwargs)
        app.initialize_server()
        app.initialize_config()
        app.initialize(argv=argv)
        app.start()
