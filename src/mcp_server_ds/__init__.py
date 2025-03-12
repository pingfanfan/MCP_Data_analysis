"""MCP Server for Data Science and Analysis"""

from .server import MCPDataServer
from .tools import (
    describe_dataset,
    clean_dataset,
    feature_engineering,
    calculate_correlations
)

__version__ = "0.1.5"
__all__ = [
    "MCPDataServer",
    "describe_dataset",
    "clean_dataset",
    "feature_engineering",
    "calculate_correlations"
] 