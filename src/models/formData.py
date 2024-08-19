from typing import Union
from pydantic import BaseModel, Field, EmailStr, field_validator

from src.models.questionData import Subjects


class UserClass(BaseModel):
    status: str

    @field_validator('status')
    def validate_status(cls, status):
        if isinstance(status, str) and status.lower() == "окончил":
            return status
        try:
            int(status)
        except:
            raise ValueError("Класс может быть либо числом, либо строкой 'окончил'.")

        else:
            if 12 > int(status) > 0:
                return status


class Named(BaseModel):
    # фамилия, имя или отчество
    name: str

    @field_validator('name')
    def validate_status(cls, value):
        if isinstance(value, str) and len(value) >= 2:
            return value
        else:
            raise ValueError("Слишком короткое имя")


class FormData(BaseModel):
    surname: Named = Field(default=None)
    name: Named = Field(default=None)
    lastname: Named = Field(default=None)
    training_class: UserClass = Field(default=None)
    school: str = Field(default=None)
    region: str = Field(default=None)
    email: EmailStr = Field(default=None)
    main_subject: Subjects = Field(default=None)
