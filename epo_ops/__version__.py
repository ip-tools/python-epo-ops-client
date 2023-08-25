try:
    from importlib.metadata import version
except ImportError:  # pragma: nocover
    from importlib_metadata import version  # type: ignore[no-redef]

__version__ = version("python-epo-ops-client")
