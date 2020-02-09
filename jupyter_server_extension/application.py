import sys

from traitlets.config.application import catch_config_error
from jupyter_server.serverapp import ServerApp
from jupyter_core.application import JupyterApp

from traitlets import Unicode, List


class ExtensionApp(JupyterApp):
    """A base class for writing Jupyter server extensions that also
    behave like stand alone Jupyter applications. 

    These applications can be loaded using jupyter_server's 
    extension loading mechanism (and `load_server_extension_function`)
    or launched using Jupyter's command line interface.

    To write an extension application, write a subclass of
    `JupyterServerExtensionApp` and a `load_jupyter_server_extension`
    function. See the example below:

    """
    # Name of the extension
    name = Unicode(
        "",
        help="Name of extension."
    )

    @default("name"):
    def _default_name(self):
        raise Exception("The extension must be given a `name`.")

    # Extension can configure the ServerApp from the command-line
    classes = [
        ServerApp
    ]

    static_paths = List(Unicode(),
        config=True,
        help="""paths to search for serving static files.
        
        This allows adding javascript/css to be available from the notebook server machine,
        or overriding individual files in the IPython
        """
    )

    template_paths = List(Unicode(), 
        config=True,
        help=_("""Paths to search for serving jinja templates.

        Can be used to override templates from notebook.templates.""")
    )


    def __init__(self, *args, **kwargs):
        self.handlers = []
        self.settings = {
            "{}_static_path".format(self.name): self.static_paths,
            "{}_template_path".format(self.name): self.template_paths
        }

    def initialize_static_handler(self):
        # Check to see if 
        if len(self.static_paths) > 0:
            handler = (
                r"/static/{}/(.*)".format(self.name),
                StaticFileHandler,
                {"path": self.static_paths}
            )
            self.handlers.append(handler)

    def initialize_handlers(self):
        pass

    def initialize_templates(self):
        pass

    def initialize_settings(self):
        pass

    # Everything below this line is for launching
    # this extension from the command line.
    # ------------------------------------------------

    def initialize_servers(self):
        """Add handlers to server."""
        self.serverapp = ServerApp()
        self.serverapp.start()

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        """Launch the ServerApp and Server Extension Application. 
        
        Properly orders the steps to initialize and start the server and extension.
        """
        # Initialize the server
        self.initialize_server()

        # Load the extension
        extension = cls.load_jupyter_server_extension(self.serverapp, argv=argv, **kwargs)
        
        # Start the application.
        extension.start()

    
    @classmethod
    def load_jupyter_server_extension(cls, serverapp, argv=None, **kwargs):
        # QUESTION: Can we update traits of ServerApp after its initialized and started?
        # Get webapp
        webapp = serverapp.web_app
        
        # Create an instance of this extension
        extension = cls.instance(**kwargs)
        extension.initialize(argv=argv)
        extension.initialize_handlers()
        extension.initialize_static_handler()
        extension.initialize_templates()
        extension.initialize_settings()

        # Make extension settings accessible to handlers inside webapp settings.
        webapp.settings.update(**extension.settings)

        # Add handlers to serverapp.
        webapp.add_handlers('.*$', extension.handlers)
