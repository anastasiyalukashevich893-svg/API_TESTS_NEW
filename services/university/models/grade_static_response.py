from pydantic import BaseModel


class GradeStaticResponse(BaseModel):
    count: int
    min: int | None
    max: int | None
    avg: float | None
