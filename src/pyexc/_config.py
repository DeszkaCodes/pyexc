"""Contains the configuration for the pyexc package that is read from the pyproject.toml file."""

from typing import Any
from pydantic import BaseModel, ConfigDict
from typing_extensions import Self

__all__ = ["PyExcConfig", "INSTANCE"]


class PyExcConfig(BaseModel):
    """The configuration for the pyexc package."""

    model_config = ConfigDict(frozen=True)

    default_exclude: list[str] = ["venv", "\\.venv", "\\.direnv", "tests", "\\.git", "setup\\.py"]
    """The default exclude patterns when searching for files to check."""

    exclude: list[str] = []
    """Additional exclude patterns when searching for files to check."""

    @classmethod
    def from_pyproject_toml_string(cls, pyproject_string: str) -> Self:
        """Create a PyExcConfig object from a pyproject.toml string.

        Args:
            pyproject_string (str): The contents of the pyproject.toml file.

        Returns:
            Self: The PyExcConfig object.
        """
        import tomli

        pyproject: dict[str, Any] = tomli.loads(pyproject_string)

        tools: Any | dict[Any, Any] = pyproject.get("tool", {})
        if not isinstance(tools, dict):
            tools = {}

        pyexc_config: Any | dict[Any, Any] = tools.get("pyexc", {})
        if not isinstance(pyexc_config, dict):
            pyexc_config = {}

        return cls.model_validate(pyexc_config)


def _get_default_config() -> PyExcConfig:
    """Get the default configuration for the pyexc package.

    Returns:
        PyExcConfig: The default configuration.
    """
    try:
        with open("pyproject.toml", "r") as file:
            pyproject_string = file.read()

        config = PyExcConfig.from_pyproject_toml_string(pyproject_string)
    except FileNotFoundError:
        config = PyExcConfig()

    return config


INSTANCE: PyExcConfig = _get_default_config()
"""The configuration for the pyexc package."""
