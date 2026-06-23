from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "employee"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    filename: str
    employee_id: Optional[int]
    summary: Optional[str]
    uploaded_by: str
    created_at: datetime

    class Config:
        from_attributes = True
