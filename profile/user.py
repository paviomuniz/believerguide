'''
Module User
'''
import datetime as dt
import uuid
# import qrcode
# import io
# import traceback
# import svgwrite
import random
from pydantic import BaseModel  #, Field
from typing import Optional  #, List
from fastapi import Depends, APIRouter, HTTPException  #, responses, Header
from fastapi.responses import StreamingResponse, Response  #, ORJSONResponse , JSONResponse

from util.dependencies import verify_api_key, ResponseItem

router = APIRouter()

PATH_PLAN_ENGAGE = "profile/user"


@router.get(
    PATH_PLAN_ENGAGE,
    tags=["profile"],
    response_model=ResponseItem,
)
async def profile_user(
        uuid: str,
        api_key: str = Depends(verify_api_key),
):
    '''
    Endpoint to return profile
    '''
    _ = api_key
    ret = ResponseItem(
        date=dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        path=PATH_PLAN_ENGAGE,
    )
    ret.data = await profile_user_db(uud)
    return ret


async def profile_user_db(uuid: str):
    '''
    Retorna o profile
    '''
    # Lista de 10 JSONs com a estrutura especificada
    json_list = [
        {
            "uuid": 'a6fa0a43-0d02-4add-bed3-a2c5d1b446cd',
            "name": "Alice",
            "country": "USA",
            "email": "alice@example.com"
        },
        {
            "uuid": '7133f00b-6b38-4f71-860c-5a49dce7f027',
            "name": "Bruno",
            "country": "Brazil",
            "email": "bruno@example.com"
        },
        {
            "uuid": 'f987d657-3e55-4387-b950-01b63b0c87f',
            "name": "Carla",
            "country": "Spain",
            "email": "carla@example.com"
        },
        {
            "uuid": '68a5fa9a-2780-4903-8079-86d60fc1707c',
            "name": "David",
            "country": "Canada",
            "email": "david@example.com"
        },
        {
            "uuid": 'e8bfb9c3-10ac-43ab-9cf6-73178185291',
            "name": "Eva",
            "country": "Germany",
            "email": "eva@example.com"
        },
        {
            "uuid": '766cc65e-3764-4974-acb9-8ac110a39390',
            "name": "Francis",
            "country": "France",
            "email": "francis@example.com"
        },
    ]

    return [x for x in json_list if x['uuid'] == uuid][0]
