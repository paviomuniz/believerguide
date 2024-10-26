'''
Dependencies for all modules
'''
import os
import datetime as dt
from typing import Optional  # , List
from pydantic import BaseModel
from fastapi import HTTPException, Header  # , responses, APIRouter, FastAPI, Depends

VALID_API_KEYS = {os.getenv("API_KEY"), 'teste123'}


def verify_api_key(api_key: Optional[str] = Header(None)):
    '''
    Verifu API key comparing with the environment variables.
    '''
    if api_key is None or api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=403,
            detail=[
                {
                    'error': True,
                    'msg': "Invalid API key",
                    'date': dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                },
            ])
    return api_key


class ResponseItem(BaseModel):
    '''
    Response structure
    '''
    date: str
    error: bool | None = False
    path: str | None = '/'
    detail: dict | None = {}
    statusCode: int | None = 200
    elapsed: float | None = 0.0
    message: str | None = 'OK'
    data: list | None = []
