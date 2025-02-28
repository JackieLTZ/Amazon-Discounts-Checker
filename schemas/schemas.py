from pydantic import BaseModel


class RequestData(BaseModel):
    browser: str
    url: str