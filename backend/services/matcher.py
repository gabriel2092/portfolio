"""
Clinical trial matching service using local or cloud LLMs
Supports both Ollama (local, free) and Anthropic Claude (cloud, paid)
"""
import logging
from typing import List, Dict, Any
import json
import httpx

from models.patient import PatientData
from models.trial import ClinicalTrial, MatchResult
from core.config import settings

logger = logging.getLogger(__name__)


class TrialMatcher:
    """Matches patients to clinical trials using AI (Ollama or Anthropic)"""

    def __init__(self):
        self.provider = settings.LLM_PROVIDER

        if self.provider == "ollama":
            self.ollama_url = settings.OLLAMA_BASE_URL
            self.model = settings.OLLAMA_MODEL
            logger.info(f"Using Ollama with model: {self.model}")
        elif self.provider == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not configured for Anthropic provider")
            from anthropic import Anthropic
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = "claude-sonnet-4-5-20250929"
            logger.info(f"Using Anthropic Claude: {self.model}")
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    def _format_patient_data(self, patient: PatientData) -> str:
        """Format patient data as readable text"""
        text = f"Patient Profile:\n"
        text += f"- Age: {patient.age} years\n"
        text += f"- Gender: {patient.gender}\n"

        if patient.conditions:
            text += f"\nMedical Conditions:\n"
            for condition in patient.conditions:
                text += f"  - {condition.name}"
                if condition.icd10_code:
                    text += f" (ICD-10: {condition.icd10_code})"
                if condition.onset_date:
                    text += f" since {condition.onset_date}"
                text += "\n"

        if patient.medications:
            text += f"\nCurrent Medications:\n"
            for med in patient.medications:
                text += f"  - {med.name}"
                if med.dosage:
                    text += f" {med.dosage}"
                if med.frequency:
                    text += f", {med.frequency}"
                text += "\n"

        if patient.lab_results:
            text += f"\nRecent Lab Results:\n"
            for lab in patient.lab_results:
                text += f"  - {lab.test_name}: {lab.value} {lab.unit}"
                if lab.date:
                    text += f" ({lab.date})"
                text += "\n"

        if patient.smoking_status:
            text += f"\nSmoking Status: {patient.smoking_status}\n"

        if patient.pregnancy_status is not None:
            text += f"Pregnancy Status: {'Pregnant' if patient.pregnancy_status else 'Not pregnant'}\n"

        return text

    def _create_prompt(self, patient_text: str, trial: ClinicalTrial) -> str:
        """Create the matching prompt for any LLM"""
        return f"""You are a clinical trial matching expert. Analyze whether a patient is eligible for a clinical trial.

{patient_text}

Clinical Trial: {trial.title}
NCT ID: {trial.nct_id}

Eligibility Criteria:
{trial.eligibility_criteria}

Your task:
1. Carefully parse the inclusion and exclusion criteria
2. Compare each criterion against the patient's data
3. Determine if the patient meets ALL inclusion criteria
4. Determine if the patient violates ANY exclusion criteria
5. Calculate an overall match score (0.0 to 1.0)
6. Provide a clear explanation

Respond in JSON format with this exact structure (no additional text):
{{
  "is_eligible": true,
  "match_score": 0.85,
  "inclusion_matches": ["criterion 1 met", "criterion 2 met"],
  "inclusion_mismatches": ["criterion X not met"],
  "exclusion_violations": ["exclusion Y violated"],
  "exclusion_passes": ["exclusion A passed", "exclusion B passed"],
  "explanation": "Brief summary for patient",
  "reasoning": "Detailed reasoning"
}}

Scoring guidance:
- 1.0 = Perfect match, all inclusion met, no exclusions violated
- 0.8-0.9 = Strong match, minor uncertainties
- 0.6-0.7 = Moderate match, some criteria unclear
- 0.4-0.5 = Weak match, significant mismatches
- 0.0-0.3 = Poor match or exclusion violated

If eligibility criteria are missing or unclear, make reasonable assumptions based on the trial title and condition.
IMPORTANT: Return ONLY the JSON object, no other text."""

    async def _call_ollama(self, prompt: str) -> str:
        """Call Ollama local API"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",  # Request JSON format
                    "options": {
                        "temperature": 0.0,  # Deterministic
                        "num_predict": 2000
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")

    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text

    async def match_patient_to_trial(
        self,
        patient: PatientData,
        trial: ClinicalTrial
    ) -> MatchResult:
        """
        Match a single patient to a single trial

        Args:
            patient: Patient data
            trial: Clinical trial

        Returns:
            MatchResult with detailed matching information
        """
        patient_text = self._format_patient_data(patient)
        prompt = self._create_prompt(patient_text, trial)

        try:
            # Call appropriate LLM provider
            if self.provider == "ollama":
                response_text = await self._call_ollama(prompt)
            else:  # anthropic
                response_text = await self._call_anthropic(prompt)

            # Parse JSON from response
            # LLMs might wrap JSON in markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            # Clean up any leading/trailing text
            response_text = response_text.strip()
            if not response_text.startswith('{'):
                # Try to find the first { and last }
                start = response_text.find('{')
                end = response_text.rfind('}')
                if start != -1 and end != -1:
                    response_text = response_text[start:end+1]

            result_data = json.loads(response_text)

            # Create MatchResult
            match_result = MatchResult(
                trial=trial,
                match_score=float(result_data.get("match_score", 0.0)),
                is_eligible=bool(result_data.get("is_eligible", False)),
                inclusion_matches=result_data.get("inclusion_matches", []),
                inclusion_mismatches=result_data.get("inclusion_mismatches", []),
                exclusion_violations=result_data.get("exclusion_violations", []),
                exclusion_passes=result_data.get("exclusion_passes", []),
                explanation=result_data.get("explanation", "Unable to determine eligibility"),
                reasoning=result_data.get("reasoning", "")
            )

            logger.info(f"Matched {trial.nct_id} using {self.provider}: score={match_result.match_score:.2f}, eligible={match_result.is_eligible}")
            return match_result

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing {self.provider} response as JSON: {e}")
            logger.error(f"Response text: {response_text[:500]}")

            # Fallback result
            return MatchResult(
                trial=trial,
                match_score=0.0,
                is_eligible=False,
                inclusion_matches=[],
                inclusion_mismatches=[],
                exclusion_violations=[],
                exclusion_passes=[],
                explanation="Error processing eligibility criteria",
                reasoning=f"LLM response parsing error: {str(e)}"
            )

        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling {self.provider}: {e}")
            if self.provider == "ollama":
                raise Exception(
                    f"Cannot connect to Ollama. Make sure Ollama is running on {self.ollama_url}. "
                    "Install from https://ollama.ai and run: ollama pull {self.model}"
                )
            raise

        except Exception as e:
            logger.error(f"Error matching patient to trial with {self.provider}: {e}")
            raise

    async def match_patient_to_trials(
        self,
        patient: PatientData,
        trials: List[ClinicalTrial],
        min_score: float = 0.0
    ) -> List[MatchResult]:
        """
        Match a patient to multiple trials

        Args:
            patient: Patient data
            trials: List of clinical trials
            min_score: Minimum match score to include (0.0 to 1.0)

        Returns:
            List of MatchResults, sorted by match score (highest first)
        """
        results = []

        for trial in trials:
            try:
                match_result = await self.match_patient_to_trial(patient, trial)

                if match_result.match_score >= min_score:
                    results.append(match_result)

            except Exception as e:
                logger.error(f"Error matching trial {trial.nct_id}: {e}")
                continue

        # Sort by match score descending
        results.sort(key=lambda x: x.match_score, reverse=True)

        logger.info(f"Matched patient to {len(results)} trials using {self.provider} (min_score={min_score})")
        return results
