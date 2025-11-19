from pydantic import BaseModel
from typing import List, Optional, Any

class UserPreferences(BaseModel):
    min_budget: Optional[int]
    max_budget: Optional[int]
    district: Optional[List[str]] = []
    location: Optional[List[str]] = []
    property_class: Optional[List[str]] = []
    property_type: Optional[List[str]] = []
    goal: Optional[str] = "investment"


class RecommendationResponse(BaseModel):
    results: List[Any]
