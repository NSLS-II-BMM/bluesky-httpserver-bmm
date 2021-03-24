from .spreadsheets import spreadsheet_to_plan_list  # noqa: F401

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
