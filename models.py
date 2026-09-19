from sqlalchemy import Column, Integer, String,UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer,primary_key=True)
    name = Column(String, nullable=False)
    
    students = relationship("Student", back_populates="department")


class Student(Base):
    __tablename__ = "students"
    
    __table_args__ = (
        UniqueConstraint("email", name="uq_students_email"),
    )
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String, nullable=False)
    email = Column(String, nullable=False)
    department_id = Column(Integer,
                           ForeignKey("departments.id",  name="fk_students_department_id"),nullable = False
                           )
    
    department = relationship("Department", back_populates="students")
    
    
