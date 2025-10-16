"""
Validation utilities for LVBK system.
"""

from typing import List, Any
import re


def validate_martial_art(martial_art: str) -> bool:
    """
    Validate martial art discipline.
    
    Args:
        martial_art: Martial art discipline name
        
    Returns:
        bool: True if valid martial art
    """
    supported_arts = [
        "silat_lincah",
        "vovinam",
        "bjj",
        "kyokushin"
    ]
    
    return martial_art.lower() in supported_arts


def validate_confidence_threshold(threshold: float) -> bool:
    """
    Validate confidence threshold value.
    
    Args:
        threshold: Confidence threshold value
        
    Returns:
        bool: True if valid threshold
    """
    return 0.0 <= threshold <= 1.0


def validate_video_format(filename: str) -> bool:
    """
    Validate video file format.
    
    Args:
        filename: Video filename
        
    Returns:
        bool: True if valid format
    """
    supported_formats = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    
    if not filename:
        return False
    
    file_ext = filename.lower().split('.')[-1]
    return f'.{file_ext}' in supported_formats


def validate_file_size(file_size: int, max_size: int = 1024 * 1024 * 1024) -> bool:
    """
    Validate file size.
    
    Args:
        file_size: File size in bytes
        max_size: Maximum allowed size in bytes
        
    Returns:
        bool: True if valid size
    """
    return 0 < file_size <= max_size


def validate_pose_sequence(pose_sequence: Any) -> bool:
    """
    Validate pose sequence data.
    
    Args:
        pose_sequence: Pose sequence data
        
    Returns:
        bool: True if valid pose sequence
    """
    try:
        import numpy as np
        
        if not isinstance(pose_sequence, np.ndarray):
            return False
        
        # Check dimensions
        if pose_sequence.ndim not in [3, 4]:
            return False
        
        # Check shape
        if pose_sequence.ndim == 3:
            # (frames, keypoints, coordinates)
            if pose_sequence.shape[1] != 17:  # Standard 17 keypoints
                return False
            if pose_sequence.shape[2] != 2:  # x, y coordinates
                return False
        elif pose_sequence.ndim == 4:
            # (frames, height, width, channels)
            if pose_sequence.shape[3] != 3:  # RGB channels
                return False
        
        return True
        
    except ImportError:
        # If numpy is not available, basic validation
        return hasattr(pose_sequence, '__len__') and len(pose_sequence) > 0


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format.
    
    Args:
        api_key: API key string
        
    Returns:
        bool: True if valid format
    """
    if not api_key:
        return False
    
    # Basic validation - should be non-empty string
    return len(api_key.strip()) > 0


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL string
        
    Returns:
        bool: True if valid URL
    """
    if not url:
        return False
    
    # Basic URL validation regex
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))

