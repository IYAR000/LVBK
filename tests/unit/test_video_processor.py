"""
Unit tests for VideoProcessor.
"""

import pytest
import numpy as np
import tempfile
import os
from unittest.mock import Mock, patch

from src.lvbk.data.video_processor import VideoProcessor


class TestVideoProcessor:
    """Test cases for VideoProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = VideoProcessor()
        self.sample_video_data = b"fake_video_data" * 1000  # 13KB of fake data
    
    def test_init(self):
        """Test processor initialization."""
        assert self.processor is not None
        assert hasattr(self.processor, 'SUPPORTED_FORMATS')
        assert hasattr(self.processor, 'MAX_FILE_SIZE')
        assert len(self.processor.SUPPORTED_FORMATS) > 0
    
    def test_supported_formats(self):
        """Test supported video formats."""
        expected_formats = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        assert self.processor.SUPPORTED_FORMATS == expected_formats
    
    def test_max_file_size(self):
        """Test maximum file size limit."""
        assert self.processor.MAX_FILE_SIZE == 1024 * 1024 * 1024  # 1GB
    
    def test_validate_video_format_valid(self):
        """Test video format validation with valid formats."""
        valid_files = [
            "test.mp4",
            "test.MOV",
            "test.avi",
            "test.mkv",
            "test.webm"
        ]
        
        for filename in valid_files:
            assert self.processor.validate_video(filename)
    
    def test_validate_video_format_invalid(self):
        """Test video format validation with invalid formats."""
        invalid_files = [
            "test.txt",
            "test.jpg",
            "test.pdf",
            "test",
            ""
        ]
        
        for filename in invalid_files:
            assert not self.processor.validate_video(filename)
    
    def test_validate_file_size_valid(self):
        """Test file size validation with valid sizes."""
        valid_sizes = [100, 1000, 1024 * 1024, 1024 * 1024 * 1024]  # Up to 1GB
        
        for size in valid_sizes:
            assert self.processor.validate_file_size(size)
    
    def test_validate_file_size_invalid(self):
        """Test file size validation with invalid sizes."""
        invalid_sizes = [0, -1, 1024 * 1024 * 1024 + 1]  # 0, negative, > 1GB
        
        for size in invalid_sizes:
            assert not self.processor.validate_file_size(size)
    
    @patch('cv2.VideoCapture')
    def test_get_video_info_success(self, mock_video_capture):
        """Test successful video info retrieval."""
        # Mock video capture
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [30.0, 900, 1920, 1080]  # fps, frame_count, width, height
        mock_cap.release.return_value = None
        mock_video_capture.return_value = mock_cap
        
        # Mock file size
        with patch('os.path.getsize', return_value=1024 * 1024):
            info = self.processor.get_video_info("test.mp4")
        
        assert info["fps"] == 30.0
        assert info["frame_count"] == 900
        assert info["width"] == 1920
        assert info["height"] == 1080
        assert info["duration"] == 30.0  # frame_count / fps
        assert info["resolution"] == "1920x1080"
        assert info["file_size"] == 1024 * 1024
    
    @patch('cv2.VideoCapture')
    def test_get_video_info_failure(self, mock_video_capture):
        """Test video info retrieval failure."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap
        
        with pytest.raises(ValueError, match="Could not open video file"):
            self.processor.get_video_info("nonexistent.mp4")
    
    @patch('cv2.VideoCapture')
    def test_validate_video_success(self, mock_video_capture):
        """Test successful video validation."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.ones((100, 100, 3), dtype=np.uint8))
        mock_cap.release.return_value = None
        mock_video_capture.return_value = mock_cap
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024):
            
            assert self.processor.validate_video("test.mp4")
    
    @patch('cv2.VideoCapture')
    def test_validate_video_invalid_format(self, mock_video_capture):
        """Test video validation with invalid format."""
        assert not self.processor.validate_video("test.txt")
    
    @patch('cv2.VideoCapture')
    def test_validate_video_too_large(self, mock_video_capture):
        """Test video validation with file too large."""
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024 * 1024 * 1024 + 1):
            
            assert not self.processor.validate_video("test.mp4")
    
    @patch('cv2.VideoCapture')
    def test_validate_video_no_frames(self, mock_video_capture):
        """Test video validation with no frames."""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)
        mock_cap.release.return_value = None
        mock_video_capture.return_value = mock_cap
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1024):
            
            assert not self.processor.validate_video("test.mp4")
    
    def test_save_temp_video(self):
        """Test temporary video file saving."""
        with patch('tempfile.mkstemp') as mock_mkstemp:
            mock_mkstemp.return_value = (1, "/tmp/test.mp4")
            
            with patch('os.fdopen') as mock_fdopen:
                mock_file = Mock()
                mock_fdopen.return_value.__enter__.return_value = mock_file
                
                result = self.processor._save_temp_video(self.sample_video_data)
                
                assert result == "/tmp/test.mp4"
                mock_file.write.assert_called_once_with(self.sample_video_data)
    
    def test_cleanup_temp_file(self):
        """Test temporary file cleanup."""
        with patch('os.path.exists', return_value=True), \
             patch('os.remove') as mock_remove:
            
            self.processor._cleanup_temp_file("/tmp/test.mp4")
            mock_remove.assert_called_once_with("/tmp/test.mp4")
    
    def test_cleanup_temp_file_not_exists(self):
        """Test cleanup of non-existent file."""
        with patch('os.path.exists', return_value=False), \
             patch('os.remove') as mock_remove:
            
            self.processor._cleanup_temp_file("/tmp/nonexistent.mp4")
            mock_remove.assert_not_called()





