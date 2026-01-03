"""
Patient data models for EMR representation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum


class Gender(str, Enum):
    """Patient gender"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Condition(BaseModel):
    """Medical condition"""
    name: str = Field(..., description="Condition name (e.g., 'Type 2 Diabetes')")
    icd10_code: Optional[str] = Field(None, description="ICD-10 code if available")
    onset_date: Optional[date] = Field(None, description="Date of diagnosis")


class Medication(BaseModel):
    """Current medication"""
    name: str = Field(..., description="Medication name")
    dosage: Optional[str] = Field(None, description="Dosage (e.g., '10mg')")
    frequency: Optional[str] = Field(None, description="Frequency (e.g., 'twice daily')")


class LabResult(BaseModel):
    """Laboratory test result"""
    test_name: str = Field(..., description="Lab test name (e.g., 'HbA1c')")
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit of measurement (e.g., '%', 'mg/dL')")
    test_date: Optional[date] = Field(None, description="Date of test")


class PatientData(BaseModel):
    """Complete patient data for trial matching"""

    # Demographics
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    gender: Gender = Field(..., description="Patient gender")

    # Medical history
    conditions: List[Condition] = Field(
        default_factory=list,
        description="List of current medical conditions"
    )

    # Current treatments
    medications: List[Medication] = Field(
        default_factory=list,
        description="Current medications"
    )

    # Lab results
    lab_results: List[LabResult] = Field(
        default_factory=list,
        description="Recent laboratory results"
    )

    # Additional context
    smoking_status: Optional[str] = Field(
        None,
        description="Smoking status (e.g., 'never', 'former', 'current')"
    )
    pregnancy_status: Optional[bool] = Field(
        None,
        description="Pregnancy status (for females)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "age": 55,
                "gender": "male",
                "conditions": [
                    {
                        "name": "Type 2 Diabetes Mellitus",
                        "icd10_code": "E11.9",
                        "onset_date": "2020-03-15"
                    }
                ],
                "medications": [
                    {
                        "name": "Metformin",
                        "dosage": "500mg",
                        "frequency": "twice daily"
                    }
                ],
                "lab_results": [
                    {
                        "test_name": "HbA1c",
                        "value": 7.5,
                        "unit": "%",
                        "test_date": "2024-01-15"
                    },
                    {
                        "test_name": "Fasting Glucose",
                        "value": 145,
                        "unit": "mg/dL",
                        "test_date": "2024-01-15"
                    }
                ],
                "smoking_status": "former"
            }
        }
