"""
API module for LVBK system.

This module contains FastAPI endpoints for martial arts technique analysis.
"""

from .main import create_app
from .endpoints import router

__all__ = ["create_app", "router"]

