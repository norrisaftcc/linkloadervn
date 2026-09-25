"""Error types for linkloader.

Parse errors happen while reading one `.scene` file, before any
cross-file checks, and always carry a file, line, and column.

Validation errors happen after every file has parsed, once the whole
story's scene graph exists. They carry a message and, where useful,
the scene label they were found in.

See docs/scene-format.md, section "Errors", for the full list of
codes each one can carry.
"""

from __future__ import annotations


class LinkLoaderError(Exception):
    """Base class for every error this package raises on purpose."""


class ParseError(LinkLoaderError):
    def __init__(self, file: str, line: int, col: int, code: str, message: str):
        self.file = file
        self.line = line
        self.col = col
        self.code = code
        self.message = message
        super().__init__(f"{file}:{line}:{col}: {code}: {message}")


class ValidationError(LinkLoaderError):
    def __init__(self, code: str, message: str, scene: str | None = None):
        self.code = code
        self.message = message
        self.scene = scene
        where = f" (scene {scene!r})" if scene else ""
        super().__init__(f"{code}: {message}{where}")


class ValidationWarning:
    """Not an exception — collected and reported, never raised."""

    def __init__(self, code: str, message: str, scene: str | None = None):
        self.code = code
        self.message = message
        self.scene = scene

    def __str__(self) -> str:
        where = f" (scene {self.scene!r})" if self.scene else ""
        return f"{self.code}: {self.message}{where}"
