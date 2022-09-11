from pydantic import BaseModel,validator,ListUniqueItemsError
import typing
import datetime
from validation_models.enums import GenderEnum

class ValidationCitizen(BaseModel):
    citizen_id: int 
    town: str 
    street: str 
    building: str 
    apartment: int 
    name: str 
    birth_date: datetime.date 
    gender: GenderEnum 
    relatives: typing.List[int]     


class CitizensList(BaseModel):
    data: typing.List[ValidationCitizen]

class Percentiles(BaseModel):
    town: str
    p50: float 
    p75: float 
    p99: float

class BirthdaysPercentile(BaseModel):
    data:typing.List[Percentiles]


# Если 1 и relatives[2,3], то 2 и 3 1

class ImportsCitizen(BaseModel):
    citizens: typing.List[ValidationCitizen]

    @validator('citizens',pre=True,always=True)
    def citizen_ids_unique(cls,v):
        print(v)
        print(cls)
        data = v
        s = set()
        for citizen in data:
            if citizen.citizen_id not in s:
                s.add(citizen.citizen_id)
            else:
                raise ListUniqueItemsError('List citizen_id should be unique')
        return v

