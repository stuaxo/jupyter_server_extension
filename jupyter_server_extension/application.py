import sys

from traitlets.config.application import catch_config_error
from jupyter_server.serverapp import ServerApp
from jupyter_core.application import JupyterApp


class JupyterServerExtensionApp(JupyterApp):
    """Subclass this application class to 
    """
    @staticmethod
    def load_jupyter_server_extension(serverapp):
        raise Exception("Must be implemented in a subclass.")

    def initialize_config(self):
        """Load configurations outside of the command line."""
        self.load_config_file()

    def initialize_server(self):
        self.serverapp = ServerApp()
        self.serverapp.initialize()
    
    @catch_config_error
    def initialize(self, argv=None):
        # don't hook up crash handler before parsing command-line
        if argv is None:
            argv = sys.argv[1:]
        if argv:
            subc = self._find_subcommand(argv[0])
            if subc:
                self.argv = argv
                self.subcommand = subc
                return
        self.parse_command_line(argv)
        self.load_jupyter_server_extension(self.serverapp)

    def start(self):
        self.serverapp.start()
        super(JupyterServerExtensionApp, self).start()

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        app = cls.instance(**kwargs)
        app.initialize_server()
        app.initialize_config()
        app.initialize(argv=argv)
        app.start()
