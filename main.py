from fastapi import FastAPI,HTTPException, Depends, Query
from sqlalchemy.orm import Session
from schemas import (StudentCreate,
                     StudentResponse,
                     StudentListResponse,
                     StudentUpdate,
                     DepartmentCreate,
                     DepartmentResponse
                     )
from database import get_db
from models import Student as StudentModel, Department
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation, ForeignKeyViolation

app = FastAPI()



    
@app.get("/students", response_model=StudentListResponse)
def get_students(
    course: str | None = None,
    min_age: int | None = None,
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(StudentModel)

    if course:
        query = query.filter(StudentModel.course == course)

    if min_age is not None:
        query = query.filter(StudentModel.age >= min_age)
        
    total = query.count()
    
    skip = (page - 1) * limit
    query = query.offset(skip).limit(limit)
    
    students = query.all()
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "students": students
    }
        



@app.post("/students",
          response_model=StudentResponse,
          status_code=201
          )
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    student_data = StudentModel(
        name=student.name,
        age=student.age,
        course=student.course,
        email=student.email,
        department_id = student.department_id
    )
    db.add(student_data)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        if isinstance(e.orig, ForeignKeyViolation):
            raise HTTPException(
                status_code=400,
                detail="Department does not exist"
            )

        raise HTTPException(
            status_code=400,
            detail="Database error"
        )
        
        db.refresh(student_data)

    return student_data

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="student not found"
        )

    return student
    
    
    
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):
    existing_student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="student not found"
        )

    update_data = student.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_student, field, value)

    db.commit()
    db.refresh(existing_student)

    return existing_student



@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="student not found"
        )

    db.delete(student)
    db.commit()

    return 




@app.post("/departments",                response_model=DepartmentResponse,
          status_code=201
          )
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    department_data = Department(
        name=department.name 
    )
    db.add(department_data)
    db.commit()
    db.refresh(department_data)
    
    return department_data
    
@app.get("/departments",response_model=list[DepartmentResponse],
        )
def get_departments(
    db: Session = Depends(get_db)
    ):
    
    departments = db.query(Department).all()
    return departments
    
    
@app.get("/departments/{department_id}",response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
    ):
    department = (db.query(Department)
                  .filter(Department.id == department_id)
                  .first()
                  )
    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department is not found"
        )

    return department













