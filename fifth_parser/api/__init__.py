"""Expose API view modules.

Import and make available all view modules within the api package.
"""

from importlib import import_module
from pkgutil import iter_modules

__all__ = [
    import_module(f"{__name__}.{module.name}.views").__name__
    for module in iter_modules(__path__)
    if module.ispkg
]
