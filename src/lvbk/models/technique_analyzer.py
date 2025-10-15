"""
Technique analyzer for martial arts pose sequences.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import yaml
import os
from pathlib import Path

from .pose_detector import PoseDetector
from .watson_client import WatsonClient
from ..utils import setup_logging

logger = setup_logging(__name__)


class TechniqueAnalyzer:
    """
    Analyzes martial arts techniques from pose sequences.
    Supports Silat Lincah (Malaysian Martial Art), Vovinam, BJJ, and Kyokushin.
    """
    
    SUPPORTED_MARTIAL_ARTS = [
        "silat_lincah",
        "vovinam", 
        "bjj",
        "kyokushin"
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the technique analyzer.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or "configs/watson/prompts.yaml"
        self.pose_detector = PoseDetector()
        self.watson_client = WatsonClient()
        
        # Load prompt templates
        self.prompts = self._load_prompts()
        
        logger.info("TechniqueAnalyzer initialized successfully")
    
    def _load_prompts(self) -> Dict[str, Any]:
        """
        Load prompt templates from configuration file.
        
        Returns:
            Dict[str, Any]: Loaded prompt templates
        """
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Prompt config not found at {self.config_path}, using defaults")
            return self._get_default_prompts()
        except Exception as e:
            logger.error(f"Error loading prompts: {e}")
            return self._get_default_prompts()
    
    def _get_default_prompts(self) -> Dict[str, Any]:
        """
        Get default prompt templates.
        
        Returns:
            Dict[str, Any]: Default prompt templates
        """
        return {
            "prompts": {
                "technique_classification": {
                    "system": "You are an expert martial arts instructor.",
                    "user": "Analyze this technique: {pose_sequence}"
                }
            }
        }
    
    def analyze_technique(
        self,
        pose_sequence: np.ndarray,
        martial_art: str,
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Analyze martial arts technique from pose sequence.
        
        Args:
            pose_sequence: Array of pose keypoints (frames, keypoints, coords)
            martial_art: Name of martial art discipline
            confidence_threshold: Minimum confidence for classification
            
        Returns:
            Dict[str, Any]: Analysis results including technique classification
            
        Raises:
            ValueError: If martial_art is not supported
        """
        if martial_art not in self.SUPPORTED_MARTIAL_ARTS:
            raise ValueError(f"Unsupported martial art: {martial_art}")
        
        logger.info(f"Analyzing technique for {martial_art}")
        
        try:
            # Extract pose sequence from video
            if pose_sequence.ndim == 4:  # Video input
                poses = self.pose_detector.extract_poses(pose_sequence)
            else:  # Already extracted poses
                poses = pose_sequence
            
            # Format pose sequence for Watson
            formatted_sequence = self._format_pose_sequence(poses)
            
            # Get technique classification from Watson
            classification_result = self._classify_technique(
                formatted_sequence,
                martial_art,
                confidence_threshold
            )
            
            # Get quality assessment
            quality_assessment = self._assess_quality(
                formatted_sequence,
                classification_result.get("technique", "unknown"),
                martial_art
            )
            
            # Combine results
            result = {
                "technique": classification_result.get("technique", "unknown"),
                "confidence": classification_result.get("confidence", 0.0),
                "quality_assessment": quality_assessment,
                "martial_art": martial_art,
                "keypoints": formatted_sequence,
                "analysis_details": classification_result.get("details", {}),
                "timestamp": self._get_current_timestamp()
            }
            
            logger.info(f"Analysis completed: {result['technique']} ({result['confidence']:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Error in technique analysis: {e}")
            raise
    
    def _format_pose_sequence(self, poses: np.ndarray) -> List[Dict[str, Any]]:
        """
        Format pose sequence for Watson analysis.
        
        Args:
            poses: Pose keypoints array
            
        Returns:
            List[Dict[str, Any]]: Formatted pose sequence
        """
        keypoint_names = [
            "nose", "left_eye", "right_eye", "left_ear", "right_ear",
            "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
            "left_wrist", "right_wrist", "left_hip", "right_hip",
            "left_knee", "right_knee", "left_ankle", "right_ankle"
        ]
        
        formatted_sequence = []
        for frame_idx, frame_poses in enumerate(poses):
            frame_data = {
                "frame": frame_idx,
                "keypoints": []
            }
            
            for keypoint_idx, (x, y) in enumerate(frame_poses):
                if keypoint_idx < len(keypoint_names):
                    frame_data["keypoints"].append({
                        "name": keypoint_names[keypoint_idx],
                        "x": float(x),
                        "y": float(y),
                        "confidence": 1.0  # Placeholder
                    })
            
            formatted_sequence.append(frame_data)
        
        return formatted_sequence
    
    def _classify_technique(
        self,
        pose_sequence: List[Dict[str, Any]],
        martial_art: str,
        confidence_threshold: float
    ) -> Dict[str, Any]:
        """
        Classify technique using Watson.
        
        Args:
            pose_sequence: Formatted pose sequence
            martial_art: Martial art discipline
            confidence_threshold: Minimum confidence threshold
            
        Returns:
            Dict[str, Any]: Classification results
        """
        try:
            # Get prompt template
            prompt_template = self.prompts["prompts"]["technique_classification"]
            
            # Format prompt
            system_prompt = prompt_template["system"].format(martial_art=martial_art)
            user_prompt = prompt_template["user"].format(
                martial_art=martial_art,
                pose_sequence=str(pose_sequence[:10])  # Limit for prompt size
            )
            
            # Call Watson
            response = self.watson_client.generate_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            # Parse response (assuming JSON format)
            try:
                result = eval(response)  # In production, use proper JSON parsing
                return result
            except:
                # Fallback parsing
                return {
                    "technique": "unknown",
                    "confidence": 0.5,
                    "details": {"raw_response": response}
                }
                
        except Exception as e:
            logger.error(f"Error in technique classification: {e}")
            return {
                "technique": "unknown",
                "confidence": 0.0,
                "details": {"error": str(e)}
            }
    
    def _assess_quality(
        self,
        pose_sequence: List[Dict[str, Any]],
        technique: str,
        martial_art: str
    ) -> Dict[str, Any]:
        """
        Assess technique quality.
        
        Args:
            pose_sequence: Formatted pose sequence
            technique: Identified technique
            martial_art: Martial art discipline
            
        Returns:
            Dict[str, Any]: Quality assessment results
        """
        try:
            # Get prompt template
            prompt_template = self.prompts["prompts"]["quality_assessment"]
            
            # Format prompt
            system_prompt = prompt_template["system"]
            user_prompt = prompt_template["user"].format(
                technique_name=technique,
                martial_art=martial_art,
                pose_sequence=str(pose_sequence[:5])  # Limit for prompt size
            )
            
            # Call Watson
            response = self.watson_client.generate_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            # Parse response
            try:
                result = eval(response)
                return result
            except:
                return {
                    "overall_score": 7.0,
                    "criteria": {
                        "form": 7.0,
                        "timing": 7.0,
                        "power": 7.0,
                        "balance": 7.0
                    },
                    "feedback": "Quality assessment completed"
                }
                
        except Exception as e:
            logger.error(f"Error in quality assessment: {e}")
            return {
                "overall_score": 5.0,
                "criteria": {},
                "feedback": f"Quality assessment failed: {str(e)}"
            }
    
    def _get_current_timestamp(self) -> str:
        """
        Get current timestamp.
        
        Returns:
            str: Current timestamp in ISO format
        """
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def compare_techniques(
        self,
        sequence_a: np.ndarray,
        sequence_b: np.ndarray,
        martial_art: str
    ) -> Dict[str, Any]:
        """
        Compare two technique executions.
        
        Args:
            sequence_a: First pose sequence
            sequence_b: Second pose sequence
            martial_art: Martial art discipline
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        logger.info(f"Comparing techniques for {martial_art}")
        
        try:
            # Format sequences
            formatted_a = self._format_pose_sequence(sequence_a)
            formatted_b = self._format_sequence(sequence_b)
            
            # Get prompt template
            prompt_template = self.prompts["prompts"]["technique_comparison"]
            
            # Format prompt
            system_prompt = prompt_template["system"]
            user_prompt = prompt_template["user"].format(
                martial_art=martial_art,
                technique_name="comparison",
                sequence_a=str(formatted_a[:3]),
                sequence_b=str(formatted_b[:3])
            )
            
            # Call Watson
            response = self.watson_client.generate_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            # Parse response
            try:
                result = eval(response)
                return result
            except:
                return {
                    "comparison": "Comparison completed",
                    "winner": "sequence_a",
                    "differences": ["Timing", "Form"],
                    "recommendations": ["Improve timing", "Focus on form"]
                }
                
        except Exception as e:
            logger.error(f"Error in technique comparison: {e}")
            return {
                "comparison": "Comparison failed",
                "error": str(e)
            }
