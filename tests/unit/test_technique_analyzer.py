"""
Unit tests for TechniqueAnalyzer.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch

from src.lvbk.models.technique_analyzer import TechniqueAnalyzer


class TestTechniqueAnalyzer:
    """Test cases for TechniqueAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = TechniqueAnalyzer()
        self.sample_poses = np.random.rand(30, 17, 2)
    
    def test_init(self):
        """Test analyzer initialization."""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, 'SUPPORTED_MARTIAL_ARTS')
        assert len(self.analyzer.SUPPORTED_MARTIAL_ARTS) == 4
    
    def test_analyze_technique_valid_martial_art(self):
        """Test technique analysis with valid martial art."""
        result = self.analyzer.analyze_technique(
            self.sample_poses,
            "silat_lincah",
            0.7
        )
        
        assert "technique" in result
        assert "confidence" in result
        assert "quality_assessment" in result
        assert "martial_art" in result
        assert result["martial_art"] == "silat_lincah"
    
    def test_analyze_technique_invalid_martial_art(self):
        """Test technique analysis with invalid martial art."""
        with pytest.raises(ValueError, match="Unsupported martial art"):
            self.analyzer.analyze_technique(
                self.sample_poses,
                "invalid_art",
                0.7
            )
    
    def test_analyze_technique_video_input(self):
        """Test technique analysis with video input."""
        video_frames = np.random.rand(30, 256, 256, 3)
        
        with patch.object(self.analyzer.pose_detector, 'extract_poses') as mock_extract:
            mock_extract.return_value = self.sample_poses
            
            result = self.analyzer.analyze_technique(
                video_frames,
                "bjj",
                0.8
            )
            
            assert result["martial_art"] == "bjj"
            mock_extract.assert_called_once()
    
    def test_format_pose_sequence(self):
        """Test pose sequence formatting."""
        formatted = self.analyzer._format_pose_sequence(self.sample_poses)
        
        assert isinstance(formatted, list)
        assert len(formatted) == 30  # Number of frames
        
        # Check first frame structure
        first_frame = formatted[0]
        assert "frame" in first_frame
        assert "keypoints" in first_frame
        assert first_frame["frame"] == 0
        assert len(first_frame["keypoints"]) == 17
    
    def test_supported_martial_arts(self):
        """Test supported martial arts list."""
        expected_arts = ["silat_lincah", "vovinam", "bjj", "kyokushin"]
        assert self.analyzer.SUPPORTED_MARTIAL_ARTS == expected_arts
    
    @patch('src.lvbk.models.technique_analyzer.yaml.safe_load')
    def test_load_prompts_file_not_found(self, mock_yaml_load):
        """Test prompt loading when file not found."""
        mock_yaml_load.side_effect = FileNotFoundError()
        
        analyzer = TechniqueAnalyzer()
        assert analyzer.prompts is not None
        assert "prompts" in analyzer.prompts
    
    def test_compare_techniques(self):
        """Test technique comparison."""
        sequence_a = np.random.rand(20, 17, 2)
        sequence_b = np.random.rand(20, 17, 2)
        
        with patch.object(self.analyzer.watson_client, 'generate_response') as mock_watson:
            mock_watson.return_value = '{"comparison": "test"}'
            
            result = self.analyzer.compare_techniques(
                sequence_a,
                sequence_b,
                "kyokushin"
            )
            
            assert "comparison" in result
            mock_watson.assert_called_once()
    
    def test_get_current_timestamp(self):
        """Test timestamp generation."""
        timestamp = self.analyzer._get_current_timestamp()
        
        assert isinstance(timestamp, str)
        assert "T" in timestamp  # ISO format
        assert len(timestamp) > 0
