from pydantic import BaseModel
from typing import Optional



class GradeStaticResponse(BaseModel):
    count: int
    min: Optional[int] = None
    max: Optional[int] = None
    avg: Optional[float] = None