"""
Patient-trial matching endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
import logging
import csv
import json
from io import StringIO
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from models.patient import PatientData
from models.trial import MatchResult
from services.clinicaltrials_client import ClinicalTrialsClient
from services.matcher import TrialMatcher

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
trials_client = ClinicalTrialsClient()
matcher = TrialMatcher()


class MatchRequest(BaseModel):
    """Request body for matching endpoint"""
    patient: PatientData
    condition: str
    max_trials: int = 10
    min_score: float = 0.0


@router.post("/match", response_model=List[MatchResult])
async def match_patient(
    patient: PatientData,
    condition: str = Query(..., description="Medical condition to search trials for"),
    max_trials: int = Query(10, ge=1, le=50, description="Maximum number of trials to match"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum match score threshold")
):
    """
    Match a patient to clinical trials

    This endpoint:
    1. Searches for trials matching the condition
    2. Uses Claude AI to match the patient against each trial's eligibility criteria
    3. Returns ranked results with match scores and explanations

    Example request body:
    ```json
    {
      "age": 55,
      "gender": "male",
      "conditions": [
        {"name": "Type 2 Diabetes Mellitus", "icd10_code": "E11.9"}
      ],
      "lab_results": [
        {"test_name": "HbA1c", "value": 7.5, "unit": "%"}
      ]
    }
    ```
    """
    try:
        # Search for trials
        logger.info(f"Searching for trials: condition={condition}")
        trials = await trials_client.search_trials(
            condition=condition,
            max_results=max_trials,
            recruiting_only=True
        )

        if not trials:
            return []

        logger.info(f"Found {len(trials)} trials, starting matching...")

        # Match patient to trials
        matches = await matcher.match_patient_to_trials(
            patient=patient,
            trials=trials,
            min_score=min_score
        )

        logger.info(f"Matched patient to {len(matches)} trials")
        return matches

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error. Please ensure ANTHROPIC_API_KEY is set."
        )
    except Exception as e:
        logger.error(f"Error matching patient: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error matching patient: {str(e)}")


@router.post("/match/{nct_id}", response_model=MatchResult)
async def match_patient_to_specific_trial(
    nct_id: str,
    patient: PatientData
):
    """
    Match a patient to a specific trial by NCT ID

    Example: POST /api/matching/match/NCT12345678
    """
    try:
        # Get the specific trial
        trial = await trials_client.get_trial_by_nct(nct_id)

        if not trial:
            raise HTTPException(status_code=404, detail=f"Trial {nct_id} not found")

        # Match patient to trial
        match_result = await matcher.match_patient_to_trial(patient, trial)

        return match_result

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error. Please ensure ANTHROPIC_API_KEY is set."
        )
    except Exception as e:
        logger.error(f"Error matching patient: {e}")
        raise HTTPException(status_code=500, detail=f"Error matching patient: {str(e)}")


@router.post("/export/csv")
async def export_matches_csv(matches: List[MatchResult]):
    """
    Export match results to CSV format

    Example request body: [list of MatchResult objects]
    """
    try:
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            "NCT ID",
            "Trial Title",
            "Match Score",
            "Is Eligible",
            "Explanation",
            "Inclusion Matches",
            "Inclusion Mismatches",
            "Exclusion Violations"
        ])

        # Write data
        for match in matches:
            writer.writerow([
                match.trial.nct_id,
                match.trial.title,
                f"{match.match_score:.2f}",
                "Yes" if match.is_eligible else "No",
                match.explanation,
                "; ".join(match.inclusion_matches),
                "; ".join(match.inclusion_mismatches),
                "; ".join(match.exclusion_violations)
            ])

        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=trial_matches.csv"}
        )

    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Error exporting CSV: {str(e)}")


@router.post("/export/json")
async def export_matches_json(matches: List[MatchResult]):
    """
    Export match results to JSON format

    Example request body: [list of MatchResult objects]
    """
    try:
        data = [match.model_dump() for match in matches]

        return StreamingResponse(
            iter([json.dumps(data, indent=2, default=str)]),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=trial_matches.json"}
        )

    except Exception as e:
        logger.error(f"Error exporting JSON: {e}")
        raise HTTPException(status_code=500, detail=f"Error exporting JSON: {str(e)}")
