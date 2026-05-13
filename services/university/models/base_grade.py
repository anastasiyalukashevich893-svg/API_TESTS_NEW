from pydantic import BaseModel, ConfigDict, Field


class MinMaxGrade:
    MIN_GRADE = 0
    MAX_GRADE = 5


class GradesCount:
    MIN_COUNT_GRADE = 2
    MAX_COUNT_GRADE = 10


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int = Field(..., ge=MinMaxGrade.MIN_GRADE, le=MinMaxGrade.MAX_GRADE)
