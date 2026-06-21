import logging
logging.basicConfig(level=logging.DEBUG)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models, schemas, crud
from app import users as user_crud
from app.auth import verify_token, verify_password, create_access_token
import traceback

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="A REST API to manage company employees",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_detail = traceback.format_exc()
    print("FULL ERROR:", error_detail)
    return JSONResponse(status_code=500, content={"error": str(exc), "detail": error_detail})

# ROOT
@app.get("/")
def root():
    return {"message": "Employee Management API is running!"}

# REGISTER
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user.name, user.email, user.password)

# LOGIN
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# PROTECTED EMPLOYEE ROUTES
@app.post("/employees", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    return crud.create_employee(db=db, employee=employee)

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    return crud.get_employees(db=db)

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    employee = crud.get_employee(db=db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    updated = crud.update_employee(db=db, employee_id=employee_id, employee=employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: str = Depends(verify_token)):
    deleted = crud.delete_employee(db=db, employee_id=employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}