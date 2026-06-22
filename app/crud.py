from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        position=employee.position,
        salary=employee.salary
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(
    db: Session,
    search: str = None,
    department: str = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(models.Employee)

    # Search by name or email
    if search:
        query = query.filter(
            or_(
                models.Employee.name.ilike(f"%{search}%"),
                models.Employee.email.ilike(f"%{search}%")
            )
        )

    # Filter by department
    if department:
        query = query.filter(
            models.Employee.department.ilike(f"%{department}%")
        )

    # Pagination
    skip = (page - 1) * limit
    total = query.count()
    employees = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "employees": employees
    }

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate):
    db_employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()
    if db_employee:
        for key, value in employee.model_dump(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee