from pydantic import BaseModel;
import json;


class StepDto(BaseModel) :

    step: str;
    data: str;
