"""
Clinical trial data models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ClinicalTrial(BaseModel):
    """Clinical trial information from ClinicalTrials.gov"""

    nct_id: str = Field(..., description="NCT identifier (e.g., 'NCT12345678')")
    title: str = Field(..., description="Official trial title")
    brief_summary: Optional[str] = Field(None, description="Brief trial summary")

    # Eligibility
    eligibility_criteria: str = Field(..., description="Raw eligibility criteria text")
    minimum_age: Optional[str] = Field(None, description="Minimum age requirement")
    maximum_age: Optional[str] = Field(None, description="Maximum age requirement")
    gender: Optional[str] = Field(None, description="Gender requirements")

    # Trial details
    phase: Optional[str] = Field(None, description="Trial phase (e.g., 'Phase 2')")
    enrollment: Optional[int] = Field(None, description="Target enrollment")
    status: Optional[str] = Field(None, description="Recruitment status")

    # Location
    locations: List[str] = Field(default_factory=list, description="Trial locations")

    # Conditions
    conditions: List[str] = Field(default_factory=list, description="Conditions studied")

    # Interventions
    interventions: List[str] = Field(default_factory=list, description="Interventions/treatments")

    class Config:
        json_schema_extra = {
            "example": {
                "nct_id": "NCT12345678",
                "title": "A Study of Drug X in Patients with Type 2 Diabetes",
                "brief_summary": "This study evaluates the safety and efficacy of Drug X...",
                "eligibility_criteria": "Inclusion Criteria:\\n- Age 18-75\\n- Diagnosed with Type 2 Diabetes\\n- HbA1c > 7%\\n\\nExclusion Criteria:\\n- Pregnant or nursing\\n- Severe kidney disease",
                "minimum_age": "18 Years",
                "maximum_age": "75 Years",
                "gender": "All",
                "phase": "Phase 2",
                "enrollment": 150,
                "status": "Recruiting",
                "locations": ["New York, NY", "Boston, MA"],
                "conditions": ["Type 2 Diabetes Mellitus"],
                "interventions": ["Drug X", "Placebo"]
            }
        }


class MatchResult(BaseModel):
    """Result of matching a patient to a clinical trial"""

    trial: ClinicalTrial = Field(..., description="The clinical trial")
    match_score: float = Field(..., ge=0, le=1, description="Match score (0-1)")
    is_eligible: bool = Field(..., description="Overall eligibility determination")

    # Detailed matching results
    inclusion_matches: List[str] = Field(
        default_factory=list,
        description="Inclusion criteria that were met"
    )
    inclusion_mismatches: List[str] = Field(
        default_factory=list,
        description="Inclusion criteria that were not met"
    )
    exclusion_violations: List[str] = Field(
        default_factory=list,
        description="Exclusion criteria that were violated (disqualifying)"
    )
    exclusion_passes: List[str] = Field(
        default_factory=list,
        description="Exclusion criteria that were passed"
    )

    # AI explanation
    explanation: str = Field(..., description="Human-readable explanation of the match")
    reasoning: Optional[str] = Field(None, description="Detailed AI reasoning")

    class Config:
        json_schema_extra = {
            "example": {
                "trial": {
                    "nct_id": "NCT12345678",
                    "title": "A Study of Drug X in Patients with Type 2 Diabetes"
                },
                "match_score": 0.85,
                "is_eligible": True,
                "inclusion_matches": [
                    "Age requirement met (patient is 55, requirement is 18-75)",
                    "Type 2 Diabetes diagnosis confirmed",
                    "HbA1c > 7% (patient: 7.5%)"
                ],
                "inclusion_mismatches": [],
                "exclusion_violations": [],
                "exclusion_passes": [
                    "Patient is not pregnant",
                    "No severe kidney disease"
                ],
                "explanation": "Patient is a strong match for this trial. All inclusion criteria are met and no exclusions apply.",
                "reasoning": "The patient meets age requirements, has the target condition with appropriate lab values, and has no disqualifying conditions."
            }
        }
