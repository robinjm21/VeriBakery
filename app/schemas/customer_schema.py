from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)]
PhoneStr = Annotated[str, StringConstraints(pattern=r"^\+?\d{7,15}$")]

class CustomerBase(BaseModel):
    name: NonEmptyStr
    phone: PhoneStr | None = None
    email: EmailStr | None = None
    address: str | None = None
    district: str | None = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: NonEmptyStr | None = None
    phone: PhoneStr | None = None
    email: EmailStr | None = None
    address: str | None = None
    district: str | None = None

class CustomerOut(CustomerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
        