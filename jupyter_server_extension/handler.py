from tornado.web import StaticFileHandler
from jupyter_server.base.handlers import JupyterHandler

from traitlets import Unicode, default

class JupyterExtensionHandler(JupyterHandler):
    """Handlers for Extensions to the Jupyter Server.
    """
    extension_name = Unicode(help="Name of the extenxsion")

    @default('extension_name')
    def _default_extension_name(self):
        raise Exception("extension_name must be set in {}.".format(self.__class__))

    @property
    def static_url_prefix(self):
        return "/static/{}/".format(self.extension_name)

    @property
    def static_path(self):
        return self.settings['{}_static_path'.format(self.extension_name)]

    def get_template(self, name):
        """Return the jinja template object for a given name"""
        return self.settings['{}_jinja2_env'.format(self.extension_name)].get_template(name)

    def static_url(self, path, include_host=None, **kwargs):
        """Returns a static URL for the given relative static file path.
        This method requires you set the ``{extension_name}_static_path`` 
        setting in your extension (which specifies the root directory 
        of your static files).
        This method returns a versioned url (by default appending
        ``?v=<signature>``), which allows the static files to be
        cached indefinitely.  This can be disabled by passing
        ``include_version=False`` (in the default implementation;
        other static file implementations are not required to support
        this, but they may support other options).
        By default this method returns URLs relative to the current
        host, but if ``include_host`` is true the URL returned will be
        absolute.  If this handler has an ``include_host`` attribute,
        that value will be used as the default for all `static_url`
        calls that do not pass ``include_host`` as a keyword argument.
        """
        self.require_setting("{}_static_path".format(self.extension_name), "static_url")

        get_url = self.settings.get(
            "static_handler_class", StaticFileHandler
        ).make_static_url

        if include_host is None:
            include_host = getattr(self, "include_host", False)

        if include_host:
            base = self.request.protocol + "://" + self.request.host
        else:
            base = ""

        # Hijack settings dict to send extension templates to extension
        # static directory.
        settings = {
            "static_path": self.static_path,
            "static_url_prefix": self.static_url_prefix
        }
        return base + get_url(settings, path, **kwargs)
