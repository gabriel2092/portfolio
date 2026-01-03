"""
Clinical trials search endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from models.trial import ClinicalTrial
from services.clinicaltrials_client import ClinicalTrialsClient

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize client
trials_client = ClinicalTrialsClient()


@router.get("/search", response_model=List[ClinicalTrial])
async def search_trials(
    condition: Optional[str] = Query(None, description="Medical condition to search for"),
    keywords: Optional[str] = Query(None, description="Additional search keywords"),
    max_results: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    recruiting_only: bool = Query(True, description="Only show recruiting trials")
):
    """
    Search for clinical trials

    Example: /api/trials/search?condition=diabetes&max_results=10
    """
    if not condition and not keywords:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'condition' or 'keywords' must be provided"
        )

    try:
        trials = await trials_client.search_trials(
            condition=condition,
            keywords=keywords,
            max_results=max_results,
            recruiting_only=recruiting_only
        )

        return trials

    except Exception as e:
        logger.error(f"Error searching trials: {e}")
        raise HTTPException(status_code=500, detail=f"Error searching trials: {str(e)}")


@router.get("/{nct_id}", response_model=ClinicalTrial)
async def get_trial(nct_id: str):
    """
    Get a specific trial by NCT ID

    Example: /api/trials/NCT12345678
    """
    try:
        trial = await trials_client.get_trial_by_nct(nct_id)

        if not trial:
            raise HTTPException(status_code=404, detail=f"Trial {nct_id} not found")

        return trial

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching trial: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching trial: {str(e)}")
