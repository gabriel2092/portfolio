"""
Client for ClinicalTrials.gov API v2
Documentation: https://clinicaltrials.gov/data-api/api
"""

import httpx
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

from models.trial import ClinicalTrial
from core.config import settings

logger = logging.getLogger(__name__)


class ClinicalTrialsClient:
    """Client for interacting with ClinicalTrials.gov API"""

    def __init__(self):
        self.base_url = settings.CLINICALTRIALS_API_URL
        self.cache_dir = Path("trials_cache")
        self.cache_enabled = settings.ENABLE_CACHE
        self.cache_expiry_hours = settings.CACHE_EXPIRY_HOURS

        if self.cache_enabled:
            self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_path(self, query_key: str) -> Path:
        """Get cache file path for a query"""
        return self.cache_dir / f"{query_key}.json"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache file is still valid"""
        if not cache_path.exists():
            return False

        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
                cached_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
                expiry_time = cached_time + timedelta(hours=self.cache_expiry_hours)
                return datetime.now() < expiry_time
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")
            return False

    def _save_to_cache(self, query_key: str, data: Any):
        """Save data to cache"""
        if not self.cache_enabled:
            return

        cache_path = self._get_cache_path(query_key)
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }

        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            logger.info(f"Saved to cache: {query_key}")
        except Exception as e:
            logger.warning(f"Error saving to cache: {e}")

    def _load_from_cache(self, query_key: str) -> Optional[Any]:
        """Load data from cache"""
        if not self.cache_enabled:
            return None

        cache_path = self._get_cache_path(query_key)

        if self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    cache_data = json.load(f)
                    logger.info(f"Loaded from cache: {query_key}")
                    return cache_data.get('data')
            except Exception as e:
                logger.warning(f"Error loading from cache: {e}")

        return None

    async def search_trials(
        self,
        condition: Optional[str] = None,
        keywords: Optional[str] = None,
        max_results: int = 20,
        recruiting_only: bool = True
    ) -> List[ClinicalTrial]:
        """
        Search for clinical trials

        Args:
            condition: Medical condition (e.g., "diabetes")
            keywords: Search keywords
            max_results: Maximum number of results to return
            recruiting_only: Only return actively recruiting trials

        Returns:
            List of ClinicalTrial objects
        """
        # Build cache key
        cache_key = f"{condition or 'none'}_{keywords or 'none'}_{max_results}_{recruiting_only}"

        # Check cache
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            return [ClinicalTrial(**trial) for trial in cached_data]

        # Build query parameters
        query_parts = []
        if condition:
            query_parts.append(f"AREA[ConditionSearch]{condition}")
        if keywords:
            query_parts.append(f"AREA[Search]{keywords}")
        if recruiting_only:
            query_parts.append("AREA[RecruitmentStatus]RECRUITING")

        query = " AND ".join(query_parts) if query_parts else None

        # Build API request
        params = {
            "format": "json",
            "pageSize": max_results,
        }

        if query:
            params["query.cond"] = condition if condition else None
            params["query.term"] = keywords if keywords else None
            params["filter.overallStatus"] = "RECRUITING" if recruiting_only else None

        # Clean None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            headers = {
                "User-Agent": "ClinicalTrialsMatchingApp/1.0 (Educational/Research Purpose)"
            }
            async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
                # Updated API v2 endpoint
                url = f"{self.base_url}/studies"
                logger.info(f"Fetching trials from ClinicalTrials.gov: {url}")

                response = await client.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                studies = data.get("studies", [])

                trials = []
                for study in studies:
                    try:
                        trial = self._parse_study(study)
                        trials.append(trial)
                    except Exception as e:
                        logger.warning(f"Error parsing study: {e}")
                        continue

                # Save to cache
                self._save_to_cache(cache_key, [trial.model_dump() for trial in trials])

                logger.info(f"Found {len(trials)} trials")
                return trials

        except Exception as e:
            logger.error(f"Error searching trials: {e}")
            raise

    def _parse_study(self, study: Dict[str, Any]) -> ClinicalTrial:
        """Parse study data from API response"""
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        description = protocol.get("descriptionModule", {})
        eligibility = protocol.get("eligibilityModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        conditions_module = protocol.get("conditionsModule", {})
        interventions_module = protocol.get("armsInterventionsModule", {})
        contacts_locations = protocol.get("contactsLocationsModule", {})

        # Extract eligibility criteria
        eligibility_criteria = eligibility.get("eligibilityCriteria", "")

        # Extract age limits
        min_age = eligibility.get("minimumAge", None)
        max_age = eligibility.get("maximumAge", None)

        # Extract gender
        gender = eligibility.get("sex", "ALL")

        # Extract locations
        locations = []
        for location in contacts_locations.get("locations", []):
            city = location.get("city", "")
            state = location.get("state", "")
            if city and state:
                locations.append(f"{city}, {state}")

        # Extract conditions
        conditions = conditions_module.get("conditions", [])

        # Extract interventions
        interventions = []
        for intervention in interventions_module.get("interventions", []):
            interventions.append(intervention.get("name", ""))

        return ClinicalTrial(
            nct_id=identification.get("nctId", ""),
            title=identification.get("briefTitle", ""),
            brief_summary=description.get("briefSummary", ""),
            eligibility_criteria=eligibility_criteria,
            minimum_age=min_age,
            maximum_age=max_age,
            gender=gender,
            phase=design.get("phases", ["N/A"])[0] if design.get("phases") else None,
            enrollment=design.get("enrollmentInfo", {}).get("count", None),
            status=status.get("overallStatus", ""),
            locations=locations[:5],  # Limit to 5 locations
            conditions=conditions,
            interventions=interventions
        )

    async def get_trial_by_nct(self, nct_id: str) -> Optional[ClinicalTrial]:
        """
        Get a specific trial by NCT ID

        Args:
            nct_id: NCT identifier (e.g., "NCT12345678")

        Returns:
            ClinicalTrial object or None if not found
        """
        cache_key = f"nct_{nct_id}"

        # Check cache
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            return ClinicalTrial(**cached_data)

        try:
            headers = {
                "User-Agent": "ClinicalTrialsMatchingApp/1.0 (Educational/Research Purpose)"
            }
            async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
                url = f"{self.base_url}/studies/{nct_id}"
                logger.info(f"Fetching trial {nct_id}")

                response = await client.get(url, params={"format": "json"})
                response.raise_for_status()

                data = response.json()
                studies = data.get("studies", [])

                if not studies:
                    return None

                trial = self._parse_study(studies[0])

                # Save to cache
                self._save_to_cache(cache_key, trial.model_dump())

                return trial

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"Trial not found: {nct_id}")
                return None
            logger.error(f"Error fetching trial: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching trial: {e}")
            raise
