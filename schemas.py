from pydantic import BaseModel, Field

class UserMatchingBase(BaseModel):
    user_id: str
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    gender: str = Field(..., min_length=1, max_length=1)
    benchpress: float = Field(..., ge=0)
    squat: float = Field(..., ge=0)
    deadlift: float = Field(..., ge=0)
    address: str
    latitude: float
    longitude: float


class UserMatchingCreate(UserMatchingBase):
    pass

class UserMatching(UserMatchingBase):
    id: int

    class Config:
        from_attributes = True

class MatchResult(BaseModel):
    user_id: str
    similarity: float
    ipf_score: float
    address: str