from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Database connection
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Define table
class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

# Request data format
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str

Base.metadata.create_all(bind=engine)

# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoint to get data
@app.get("/emp")
def get_users(db: Session = Depends(get_db)):
    emps = db.query(Employee).all()

    return [
        {"employee_id": emp.employee_id, "first_name": emp.first_name, "last_name": emp.last_name}
        for emp in emps
    ]

@app.post("/emp")
def add_emp(emp: EmployeeCreate, db: Session = Depends(get_db)):
    new_emp = Employee(
        first_name=emp.first_name,
        last_name=emp.last_name
    )

    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return {
        "message": "Employee added successfully",
        "employee_id": new_emp.employee_id,
        "first_name": new_emp.first_name,
        "last_name": new_emp.last_name
    }
