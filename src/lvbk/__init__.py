"""
LVBK Martial Arts Computer Vision AI System

A comprehensive AI system for analyzing martial arts techniques through computer vision,
supporting Silat Lincah, Vovinam Viet Vo Dao, Brazilian Jiu-Jitsu, and Kyokushin Nakamura.
"""

__version__ = "0.1.0"
__author__ = "LVBK Development Team"
__email__ = "lvbk@example.com"

# Import main components for easy access
from .api import create_app
from .models import TechniqueAnalyzer
from .data import VideoProcessor
from .utils import setup_logging

__all__ = [
    "create_app",
    "TechniqueAnalyzer", 
    "VideoProcessor",
    "setup_logging",
    "__version__",
    "__author__",
    "__email__"
]
