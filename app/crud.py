from sqlalchemy.orm import Session
from app import models, schemas

# CREATE - Add new employee
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

# READ - Get all employees
def get_employees(db: Session):
    return db.query(models.Employee).all()

# READ - Get one employee by ID
def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

# UPDATE - Update employee
def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee:
        for key, value in employee.model_dump(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

# DELETE - Delete employee
def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee