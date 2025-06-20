"""
This type stub file was generated by pyright.
"""

import importlib.metadata as importlib_metadata
import os
import warnings
from collections.abc import Iterable
from typing import Final, TYPE_CHECKING
from . import PydanticPluginProtocol

if TYPE_CHECKING:
    ...
PYDANTIC_ENTRY_POINT_GROUP: Final[str] = ...
_plugins: dict[str, PydanticPluginProtocol] | None = ...
_loading_plugins: bool = ...
def get_plugins() -> Iterable[PydanticPluginProtocol]:
    """Load plugins for Pydantic.

    Inspired by: https://github.com/pytest-dev/pluggy/blob/1.3.0/src/pluggy/_manager.py#L376-L402
    """
    ...

