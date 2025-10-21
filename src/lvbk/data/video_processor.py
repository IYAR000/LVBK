"""
Video processing utilities for martial arts analysis.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import cv2
from pathlib import Path
import tempfile
import os

from ..utils import setup_logging

logger = setup_logging(__name__)


class VideoProcessor:
    """
    Processes video files for martial arts technique analysis.
    """
    
    SUPPORTED_FORMATS = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB
    
    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize video processor.
        
        Args:
            temp_dir: Directory for temporary files
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.supported_codecs = ['h264', 'h265', 'vp8', 'vp9']
        
        logger.info(f"VideoProcessor initialized with temp dir: {self.temp_dir}")
    
    def process_video(self, video_data: bytes) -> np.ndarray:
        """
        Process video data and extract frames.
        
        Args:
            video_data: Raw video data bytes
            
        Returns:
            np.ndarray: Processed video frames
            
        Raises:
            ValueError: If video format is not supported
            ValueError: If video file is too large
        """
        try:
            # Validate file size
            if len(video_data) > self.MAX_FILE_SIZE:
                raise ValueError(f"Video file too large. Maximum size: {self.MAX_FILE_SIZE} bytes")
            
            # Save video to temporary file
            temp_video_path = self._save_temp_video(video_data)
            
            try:
                # Extract frames
                frames = self._extract_frames(temp_video_path)
                
                # Process frames
                processed_frames = self._process_frames(frames)
                
                logger.info(f"Video processed successfully: {processed_frames.shape}")
                return processed_frames
                
            finally:
                # Clean up temporary file
                self._cleanup_temp_file(temp_video_path)
                
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            raise
    
    def _save_temp_video(self, video_data: bytes) -> str:
        """
        Save video data to temporary file.
        
        Args:
            video_data: Raw video data
            
        Returns:
            str: Path to temporary video file
        """
        try:
            # Create temporary file
            temp_fd, temp_path = tempfile.mkstemp(
                suffix='.mp4',
                dir=self.temp_dir
            )
            
            # Write video data
            with os.fdopen(temp_fd, 'wb') as f:
                f.write(video_data)
            
            logger.debug(f"Video saved to temporary file: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Error saving temporary video: {e}")
            raise
    
    def _extract_frames(self, video_path: str) -> List[np.ndarray]:
        """
        Extract frames from video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            List[np.ndarray]: List of video frames
        """
        try:
            # Open video file
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            frames = []
            frame_count = 0
            max_frames = 1000  # Limit frames for processing
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Limit number of frames
                if frame_count >= max_frames:
                    break
                
                frames.append(frame)
                frame_count += 1
            
            cap.release()
            
            if not frames:
                raise ValueError("No frames extracted from video")
            
            logger.info(f"Extracted {len(frames)} frames from video")
            return frames
            
        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            raise
    
    def _process_frames(self, frames: List[np.ndarray]) -> np.ndarray:
        """
        Process extracted frames.
        
        Args:
            frames: List of video frames
            
        Returns:
            np.ndarray: Processed frames array
        """
        try:
            if not frames:
                raise ValueError("No frames to process")
            
            # Convert to numpy array
            frames_array = np.array(frames)
            
            # Resize frames to standard size
            processed_frames = []
            target_size = (256, 256)
            
            for frame in frames_array:
                # Resize frame
                resized_frame = cv2.resize(frame, target_size)
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                
                processed_frames.append(rgb_frame)
            
            processed_array = np.array(processed_frames)
            
            logger.info(f"Processed frames shape: {processed_array.shape}")
            return processed_array
            
        except Exception as e:
            logger.error(f"Error processing frames: {e}")
            raise
    
    def _cleanup_temp_file(self, file_path: str) -> None:
        """
        Clean up temporary file.
        
        Args:
            file_path: Path to temporary file
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Could not clean up temporary file {file_path}: {e}")
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """
        Get video file information.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dict[str, Any]: Video information
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            info = {
                "fps": fps,
                "frame_count": frame_count,
                "width": width,
                "height": height,
                "duration": duration,
                "resolution": f"{width}x{height}",
                "file_size": os.path.getsize(video_path) if os.path.exists(video_path) else 0
            }
            
            logger.info(f"Video info: {info}")
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            raise
    
    def validate_video(self, video_path: str) -> bool:
        """
        Validate video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            bool: True if video is valid
        """
        try:
            # Check file extension
            file_ext = Path(video_path).suffix.lower()
            if file_ext not in self.SUPPORTED_FORMATS:
                logger.error(f"Unsupported video format: {file_ext}")
                return False
            
            # Check file size
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                if file_size > self.MAX_FILE_SIZE:
                    logger.error(f"Video file too large: {file_size} bytes")
                    return False
            
            # Check if video can be opened
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                logger.error(f"Could not open video file: {video_path}")
                return False
            
            # Check if video has frames
            ret, frame = cap.read()
            if not ret or frame is None:
                logger.error("Video file has no valid frames")
                cap.release()
                return False
            
            cap.release()
            
            logger.info(f"Video validation successful: {video_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error validating video: {e}")
            return False
    
    def extract_key_frames(self, video_path: str, num_frames: int = 10) -> List[np.ndarray]:
        """
        Extract key frames from video.
        
        Args:
            video_path: Path to video file
            num_frames: Number of key frames to extract
            
        Returns:
            List[np.ndarray]: List of key frames
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get total frame count
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Calculate frame indices to extract
            if total_frames <= num_frames:
                frame_indices = list(range(total_frames))
            else:
                frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            
            key_frames = []
            
            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    # Convert BGR to RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    key_frames.append(rgb_frame)
            
            cap.release()
            
            logger.info(f"Extracted {len(key_frames)} key frames")
            return key_frames
            
        except Exception as e:
            logger.error(f"Error extracting key frames: {e}")
            raise
    
    def create_thumbnail(self, video_path: str, timestamp: float = 0.0) -> np.ndarray:
        """
        Create thumbnail from video at specified timestamp.
        
        Args:
            video_path: Path to video file
            timestamp: Timestamp in seconds
            
        Returns:
            np.ndarray: Thumbnail image
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Set frame position
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(timestamp * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            # Read frame
            ret, frame = cap.read()
            
            if not ret:
                raise ValueError(f"Could not read frame at timestamp {timestamp}")
            
            cap.release()
            
            # Convert BGR to RGB
            thumbnail = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            logger.info(f"Created thumbnail at timestamp {timestamp}")
            return thumbnail
            
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            raise





