from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Student CRUD API", version="1.0.0")


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=1, le=120)
    course: str = Field(..., min_length=1, max_length=100)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    id: int


# In-memory store: {id: Student}
students: Dict[int, Student] = {}
_next_id = 1


def _email_taken(email: str, exclude_id: Optional[int] = None) -> bool:
    return any(
        s.email.lower() == email.lower() and s.id != exclude_id
        for s in students.values()
    )


@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate):
    global _next_id
    if _email_taken(payload.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    student = Student(id=_next_id, **payload.model_dump())
    students[student.id] = student
    _next_id += 1
    return student


@app.get("/students", response_model=List[Student])
def list_students():
    return list(students.values())


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    student = students.get(student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    return student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, payload: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    if _email_taken(payload.email, exclude_id=student_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    updated = Student(id=student_id, **payload.model_dump())
    students[student_id] = updated
    return updated


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    del students[student_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
