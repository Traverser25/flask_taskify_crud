from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[int] = None
    status: Optional[int] = None
    assigned_to: Optional[int] = None

    @validator('priority')
    def validate_priority(cls, v):
        if v not in [1, 2]:  # Validating that priority should be either 1 (low) or 2 (high)
            raise ValueError('Priority must be 1 (low) or 2 (high)')
        return v

    @validator('status')
    def validate_status(cls, v):
        if v not in [1, 2, 3, 4]:  # Validating status range (1-4)
            raise ValueError('Status must be between 1 and 4')
        return v

    class Config:
        anystr_strip_whitespace = True  # Strips leading/trailing whitespace from string fields
