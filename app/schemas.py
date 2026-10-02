from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints

NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
StudentIdStr = Annotated[str, StringConstraints(pattern=r"^S\d{7}$")]

class UserCreate(BaseModel):
    userid: int = Field(gt=0)
    name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    email: EmailStr
    age: int = Field(gt=18, lt=120)
    student_id: Annotated[str, StringConstraints(pattern=r"^S\d{7}$")]


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: NameStr
    email: EmailStr
    age: StudentIdStr                                                