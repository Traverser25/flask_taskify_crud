from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: int
    status: int
    assigned_to: int 

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
        anystr_strip_whitespace = True
