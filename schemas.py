from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    name: str
    age: int = Field(gt=0, le=100)
    course: str
    email: EmailStr
    department_id: int

class DepartmentCreate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str
    email: str
    department_id: int
    department: DepartmentResponse

    model_config = ConfigDict(from_attributes=True)  #this line means "Configure this Pydantic model so that it can read values from object attributes."
    
class StudentListResponse(BaseModel):
    page: int
    limit: int
    total: int
    students: list[StudentResponse]
    
    
class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = Field(default = None, gt=0, le=100)
    course: str | None = None
    email: EmailStr | None = None
    

