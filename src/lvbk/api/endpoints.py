"""
API endpoints for LVBK system.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import uuid
import os
from datetime import datetime

from ..models import TechniqueAnalyzer
from ..data import VideoProcessor
from ..utils import setup_logging

logger = setup_logging(__name__)
router = APIRouter()

# Initialize components
analyzer = TechniqueAnalyzer()
video_processor = VideoProcessor()

# In-memory storage for demo (replace with database in production)
analysis_results = {}


@router.post("/analyze")
async def analyze_technique(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    martial_art: str = Form(...),
    confidence_threshold: float = Form(0.7)
) -> Dict[str, Any]:
    """
    Analyze martial arts technique from uploaded video.
    
    Args:
        background_tasks: FastAPI background tasks
        video: Uploaded video file
        martial_art: Martial art discipline (silat_lincah, vovinam, bjj, kyokushin)
        confidence_threshold: Minimum confidence threshold for analysis
        
    Returns:
        Dict[str, Any]: Analysis results including technique classification
    """
    try:
        # Validate martial art
        supported_arts = ["silat_lincah", "vovinam", "bjj", "kyokushin"]
        if martial_art not in supported_arts:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported martial art. Supported: {supported_arts}"
            )
        
        # Validate file size (1GB limit)
        max_size = 1024 * 1024 * 1024  # 1GB
        video_content = await video.read()
        if len(video_content) > max_size:
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size is 1GB."
            )
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Store analysis metadata
        analysis_results[analysis_id] = {
            "id": analysis_id,
            "status": "processing",
            "martial_art": martial_art,
            "confidence_threshold": confidence_threshold,
            "created_at": datetime.utcnow().isoformat(),
            "filename": video.filename
        }
        
        # Process video in background
        background_tasks.add_task(
            process_video_analysis,
            analysis_id,
            video_content,
            martial_art,
            confidence_threshold
        )
        
        return {
            "analysis_id": analysis_id,
            "status": "processing",
            "message": "Video analysis started. Use the analysis_id to check results."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_technique: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analysis/{analysis_id}")
async def get_analysis_result(analysis_id: str) -> Dict[str, Any]:
    """
    Get analysis results by ID.
    
    Args:
        analysis_id: Unique analysis identifier
        
    Returns:
        Dict[str, Any]: Analysis results or status
    """
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    result = analysis_results[analysis_id]
    
    if result["status"] == "processing":
        return {
            "analysis_id": analysis_id,
            "status": "processing",
            "message": "Analysis is still in progress. Please check again later."
        }
    
    return result


@router.get("/analysis")
async def list_analyses(
    limit: int = 10,
    offset: int = 0,
    martial_art: Optional[str] = None
) -> Dict[str, Any]:
    """
    List recent analyses with optional filtering.
    
    Args:
        limit: Maximum number of results to return
        offset: Number of results to skip
        martial_art: Filter by martial art discipline
        
    Returns:
        Dict[str, Any]: List of analyses with pagination info
    """
    try:
        # Filter analyses
        filtered_results = []
        for result in analysis_results.values():
            if martial_art and result.get("martial_art") != martial_art:
                continue
            filtered_results.append(result)
        
        # Sort by creation time (newest first)
        filtered_results.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Apply pagination
        total = len(filtered_results)
        paginated_results = filtered_results[offset:offset + limit]
        
        return {
            "analyses": paginated_results,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
        
    except Exception as e:
        logger.error(f"Error in list_analyses: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str) -> Dict[str, str]:
    """
    Delete analysis by ID.
    
    Args:
        analysis_id: Unique analysis identifier
        
    Returns:
        Dict[str, str]: Confirmation message
    """
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    del analysis_results[analysis_id]
    return {"message": "Analysis deleted successfully"}


@router.get("/martial_arts")
async def get_supported_martial_arts() -> Dict[str, Any]:
    """
    Get list of supported martial arts disciplines.
    
    Returns:
        Dict[str, Any]: Supported martial arts with descriptions
    """
    return {
        "martial_arts": [
            {
                "id": "silat_lincah",
                "name": "Silat Lincah",
                "description": "Malaysian Martial Art with fluid movements",
                "techniques": ["Langkah Tiga", "Jurus", "Bunga Sembah"]
            },
            {
                "id": "vovinam",
                "name": "Vovinam Viet Vo Dao",
                "description": "Vietnamese martial art combining hard and soft techniques",
                "techniques": ["Basic forms", "Self-defense techniques"]
            },
            {
                "id": "bjj",
                "name": "Brazilian Jiu-Jitsu",
                "description": "Ground-based grappling martial art",
                "techniques": ["Guard passes", "Submissions", "Escapes"]
            },
            {
                "id": "kyokushin",
                "name": "Kyokushin Nakamura",
                "description": "Full-contact karate style with powerful strikes",
                "techniques": ["Kicks", "Punches", "Kata forms"]
            }
        ]
    }


async def process_video_analysis(
    analysis_id: str,
    video_content: bytes,
    martial_art: str,
    confidence_threshold: float
) -> None:
    """
    Process video analysis in background.
    
    Args:
        analysis_id: Unique analysis identifier
        video_content: Video file content
        martial_art: Martial art discipline
        confidence_threshold: Confidence threshold for analysis
    """
    try:
        logger.info(f"Starting analysis for {analysis_id}")
        
        # Update status to processing
        analysis_results[analysis_id]["status"] = "processing"
        
        # Process video
        processed_video = video_processor.process_video(video_content)
        
        # Analyze technique
        analysis_result = analyzer.analyze_technique(
            processed_video,
            martial_art,
            confidence_threshold
        )
        
        # Update results
        analysis_results[analysis_id].update({
            "status": "completed",
            "result": analysis_result,
            "completed_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Analysis completed for {analysis_id}")
        
    except Exception as e:
        logger.error(f"Error processing analysis {analysis_id}: {str(e)}")
        analysis_results[analysis_id].update({
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.utcnow().isoformat()
        })
