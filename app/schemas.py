from pydantic import BaseModel
from typing import Optional, List

class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str
    position: str
    salary: float

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None

class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str
    department: str
    position: str
    salary: float

    class Config:
        from_attributes = True

class EmployeeListResponse(BaseModel):
    total: int
    page: int
    limit: int
    employees: List[EmployeeOut]
