# app/routes/student_routes.py
from fastapi import APIRouter, HTTPException
from app.models.student_model import Student
from app.database import students


router = APIRouter(prefix="/students", tags=["Students"])


# ✅ CREATE
@router.post("/", response_model=Student)
def create_student(student: Student):
    # check if ID already exists
    for s in students:
        if s["id"] == student.id:
            raise HTTPException(status_code=400, detail="Student ID already exists")
    students.append(student.model_dump())
    return student


# ✅ READ ALL
@router.get("/", response_model=list[Student])
def get_all_students():
    return students


# ✅ READ ONE
@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")


# ✅ UPDATE
@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, updated_data: Student):
    for index, s in enumerate(students):
        if s["id"] == student_id:
            students[index] = updated_data.model_dump()
            return updated_data
    raise HTTPException(status_code=404, detail="Student not found")


# ✅ DELETE
@router.delete("/{student_id}")
def delete_student(student_id: int):
    for index, s in enumerate(students):
        if s["id"] == student_id:
            del students[index]
            return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")
