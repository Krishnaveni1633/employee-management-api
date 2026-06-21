from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# What data is needed to CREATE an employee
class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str
    position: str
    salary: float

# What data is needed to UPDATE an employee
class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None

# What data we SEND BACK in response
class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    position: str
    salary: float
    created_at: datetime

    class Config:
        from_attributes = True

        # User schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None