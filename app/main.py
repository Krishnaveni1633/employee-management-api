import logging
logging.basicConfig(level=logging.DEBUG)

from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.email import send_welcome_email, send_employee_added_email, send_document_summary_email
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import engine, Base, get_db
from app import models, schemas, crud
from app import users as user_crud
from app.auth import verify_password, create_access_token, get_current_user, require_role
from app.documents import extract_text_from_pdf, summarize_with_ai
import traceback

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="Full stack Employee Management System with AI Document Summarization, JWT authentication, and React frontend",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_detail = traceback.format_exc()
    print("FULL ERROR:", error_detail)
    return JSONResponse(status_code=500, content={"error": str(exc), "detail": error_detail})

@app.get("/")
def root():
    return {"message": "Employee Management API is running!"}

@app.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user_crud.create_user(db, user.name, user.email, user.password, user.role)
    # Send welcome email
    await send_welcome_email(new_user.email, new_user.name)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@app.post("/employees", response_model=schemas.EmployeeOut)
async def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    new_employee = crud.create_employee(db=db, employee=employee)
    # Send notification email
    await send_employee_added_email(current_user.email, new_employee.name)
    return new_employee

@app.get("/employees", response_model=schemas.EmployeeListResponse)
def get_employees(
    search: Optional[str] = None,
    department: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager"))
):
    return crud.get_employees(db, search=search, department=department, page=page, limit=limit)

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager"))
):
    emp = crud.update_employee(db, employee_id, employee)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    emp = crud.delete_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": f"Employee {employee_id} deleted successfully"}

@app.post("/documents/upload", response_model=schemas.DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    employee_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager"))
):
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    summary = summarize_with_ai(text)

    db_document = models.Document(
        filename=file.filename,
        employee_id=employee_id,
        summary=summary,
        uploaded_by=current_user.email
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Send summary email
    await send_document_summary_email(
        current_user.email,
        file.filename,
        summary
    )

    return db_document

@app.get("/documents", response_model=List[schemas.DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("manager"))
):
    return db.query(models.Document).all()

@app.get("/documents/{document_id}", response_model=schemas.DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doc = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc