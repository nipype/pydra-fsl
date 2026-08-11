from .._version import __version__  # noqa: F401
from fileformats.generic import File, Directory


class Con(File):
    ext = ".con"
    binary = True


class MelodicIca(Directory):
    """Directory containing output from Melodic ICA"""
