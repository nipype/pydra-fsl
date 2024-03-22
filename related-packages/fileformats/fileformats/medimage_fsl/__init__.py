from ._version import __version__  # noqa: F401
from fileformats.generic import File

class Con(File):
    ext = ".con"
    binary = True
