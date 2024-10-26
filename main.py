'''
* Believers Guide
* objective: Create endpoint for curd operations in python for Believers Guide 
'''
# import fastapi
import datetime as dt
# from typing import Optional
import os
from typing import List
# import re
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException  # , Header, responses, APIRouter, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from profile import crud, schemas  # , models, user
from services.scheduler import scheduler
from util.dependencies import verify_api_key, ResponseItem
from util.database import SessionLocal, engine, Base
from journey.models import Journey, Activity
from journey.crud import create_journey, get_journey, update_journey, delete_journey
from journey.schemas import (
    JourneyCreate,
    JourneyBase,
    Journey,
    Activity,
    ActivityBase,
    ActivityCreate,
)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# _ = scheduler

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "https://zion-app-giving.flutterflow.app",
    # Adicione outros domínios conforme necessário
]

PROFILING = os.getenv("PROFILE")

app = FastAPI(
    title="Believer Guide 0.1",
    root_path='/',
    # dependencies=[Depends(verify_api_key)],
)
# app.include_router(user.router)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get('/ping')
async def index(message: str):
    '''
    Test endpoint
    '''
    return {"pong": message}


# Register an event for application startup
# @app.on_event("startup")
# async def startup_event():
#     scheduler.start()


# @app.on_event("shutdown")
# async def shutdown_event():
#     scheduler.shutdown()


# Definindo o modelo
class Uuid(BaseModel):
    uuid: str


@app.post('/profile/user')
async def profile_user(
    uuid: Uuid,
    api_key: str = Depends(verify_api_key),
):
    '''
    Endpoint to return profile
    '''
    _ = api_key
    ret = ResponseItem(
        date=dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        path='/profile/user',
    )
    ret.data = await profile_user_db(uuid.uuid)
    return ret


async def profile_user_db(uuid: str) -> List:
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


@app.post("/profile/user/create", response_model=schemas.ProfileResponse)
def create_profile(profile: schemas.ProfileCreate,
                   db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile)


@app.get("/profile/user/{profile_uuid}", response_model=schemas.ProfileResponse)
def read_profile(profile_uuid: str, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_uuid=profile_uuid)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.put("/profile/user/{profile_uuid}", response_model=schemas.ProfileResponse)
def update_profile(profile_uuid: str,
                   profile: schemas.ProfileCreate,
                   db: Session = Depends(get_db)):
    db_profile = crud.update_profile(db,
                                    profile_uuid=profile_uuid,
                                    profile=profile)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.delete("/profile/user/{profile_uuid}", response_model=schemas.ProfileResponse)
def delete_profile(profile_uuid: str, db: Session = Depends(get_db)):
    db_profile = crud.delete_profile(db, profile_uuid=profile_uuid)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.post('/journey/list')
async def journey_list(api_key: str = Depends(verify_api_key), ):
    '''
    Endpoint to return journet
    '''
    _ = api_key
    ret = ResponseItem(
        date=dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        path='/journey/list',
    )
    ret.data = await journey_list_db()
    return ret


async def journey_list_db():
    '''
    Retorna o profile
    '''
    # Lista de 10 JSONs com a estrutura especificada

    json_list = [
        {
            "theme":
            "Noah's Ark",
            "description": "Salvation is like Noah’s ark that has no rudder. It means we don’t have control over our salvation",
            "activities": [
                {
                    "id": "867681a7-2267-4c85-8b08-53b1446f9e58",
                    "status": "not_started"
                }, {
                    "id": "144ad336-2eeb-4027-8cb3-f342ee108a6d",
                    "status": "not_started"
                }, {
                    "id": "3454fa93-c928-49d3-b053-3ab60fa7ac3e",
                    "status": "not_started"
                }]
        },
        {
            "theme": "Jonah's Boat",
            "description": "Obedience as a principle",
            "activities": [
                {
                    "id": "02632ed9-7a31-49b2-ad95-b4cb01c9966c",
                    "status": "not_started"
                }, {
                    "id": "e03d5798-e535-4f7d-a697-6bc1b66e8b06",
                    "status": "not_started"
                }, {
                    "id": "98744c7b-ce2f-41dd-a466-19665b0985b7",
                    "status": "not_started"
                }
            ]
        },
        {
            "theme": "Disciple's Boat",
            "description": "Confidance in Jesus Christ",
            "activities": [
                {
                    "id": "54c5f853-6bfd-4ea1-bd68-5d01029e7ca1",
                    "status": "not_started"
                }, {
                    "id": "ea979248-e18b-4442-9379-186c2780f2b2",
                    "status": "not_started"
                }, {
                    "id": "a2794fca-d37d-4c85-a70e-aff5f34bb417",
                    "status": "not_started"
                }
            ]
        },
        {
            "theme": "Pauls's Boat",
            "description": "Bear fruit of Holy Spirit",
            "activities": [
                {
                    "id": "40ade95a-325e-45e4-89e6-e76486e7c79c",
                    "status": "not_started"
                }, {
                    "id": "cab8a3c5-d7ed-4c14-a4d9-6238289daf72",
                    "status": "not_started"
                }, {
                    "id": "d157d28e-625b-4821-80d8-406be281a3ab",
                    "status": "not_started"
                }
            ]
        },
    ]

    return json_list


##############################
# Endpoints para o CRUD
@app.post("/journey/create", response_model=JourneyCreate)
def create_journey(journey: JourneyCreate, db: Session = Depends(get_db)):

    return create_journey(db,journey=journey)


@app.get("/journey", response_model=List[Journey])
def read_journey_list(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    '''
    journey get
    '''
    return db.query(Journey).offset(skip).limit(limit).all()


@app.get("/journey/{journey_id}", response_model=Journey)
def read_journey(journey_id: str, db: Session = Depends(get_db)):
    db_journey = get_journey(db, journey_id)
    if db_journey is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_journey


@app.put("/journey/{journey_id}", response_model=Journey)
def update_profile(journey_id: str, journey: Journey, db: Session = Depends(get_db)):
    db_journey = update_journey(db, journey_id, journey)
    if db_journey is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return db_journey

@app.delete("/journey/{profile_id}")
def delete_profile(journey_id: str, db: Session = Depends(get_db)):
    db_journey = delete_journey(db, journey_id)
    if db_journey is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return db_journey

# # Definindo o modelo
# class Uuid(BaseModel):
#   uuid: str


@app.post('/journey/activities')
async def journey_activities(
    uuid: Uuid,
    api_key: str = Depends(verify_api_key),
):
    '''
    Endpoint to return journet
    '''
    _ = api_key
    ret = ResponseItem(
        date=dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        path='/journey/activities',
    )
    ret.data = await journey_activities_db(uuid.uuid)
    return ret


async def journey_activities_db(uuid: str):
    json_list = [
        {
            "id": "867681a7-2267-4c85-8b08-53b1446f9e58",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "144ad336-2eeb-4027-8cb3-f342ee108a6d",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "3454fa93-c928-49d3-b053-3ab60fa7ac3e",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started",
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started",
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "02632ed9-7a31-49b2-ad95-b4cb01c9966c",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "e03d5798-e535-4f7d-a697-6bc1b66e8b06",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "98744c7b-ce2f-41dd-a466-19665b0985b7",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "54c5f853-6bfd-4ea1-bd68-5d01029e7ca1",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "ea979248-e18b-4442-9379-186c2780f2b2",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "a2794fca-d37d-4c85-a70e-aff5f34bb417",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "40ade95a-325e-45e4-89e6-e76486e7c79c",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "cab8a3c5-d7ed-4c14-a4d9-6238289daf72",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
        {
            "id": "d157d28e-625b-4821-80d8-406be281a3ab",
            "status": "not_started",
            "title": "God is Creator",
            "video": {
                "title": "God is Creator",
                "url": "https://www.youtube.com/watch?v=NIjlr-1TlDQ",
                "status": "not_started"
            },
            "text": {
                "title": "Man Is Sinful",
                "description":
                "All have sinned and fall short of the glory of God (Romans 3:23).",
                "status": "not_started"
            },
            "quiz": {
                "title": "God of covenant",
                "id": "e97e116c-92ac-498f-992d-084bf3a3c49b"
            },
        },
    ]
    return [x for x in json_list if x['id'] == uuid][0]


# # Definindo o modelo
# class Uuid(BaseModel):
#   uuid: str


@app.post('/journey/quiz')
async def journey_quiz(
    uuid: Uuid,
    api_key: str = Depends(verify_api_key),
):
    '''
    Endpoint to return quiz
    '''
    _ = api_key
    ret = ResponseItem(
        date=dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        path='/journey/quiz',
    )
    ret.data = await journey_quiz_db(uuid.uuid)
    return ret


async def journey_quiz_db(uuid: str):
    json_list = [{
        "question":
        "What is the main purpose of the 'New Beginnings: The First Six Months' section in the app?",
        "answer_id":
        2,
        "options": [{
            "id": 0,
            "text": "To provide entertainment for new believers."
        }, {
            "id": 1,
            "text": "To offer advanced theological training."
        }, {
            "id":
            2,
            "text":
            "To establish a strong spiritual foundation for new believers."
        }, {
            "id": 3,
            "text": "To help new believers learn a new language."
        }, {
            "id": 4,
            "text": "To promote a fitness program for Christians."
        }]
    }, {
        "question":
        "Which feature helps new believers track their progress in spiritual disciplines?",
        "answer_id":
        3,
        "options": [{
            "id": 0,
            "text": "Bible study sessions."
        }, {
            "id": 1,
            "text": "Weekly video tutorials."
        }, {
            "id": 2,
            "text": "Daily inspirational quotes."
        }, {
            "id": 3,
            "text": "Spiritual Disciplines Tracker."
        }, {
            "id": 4,
            "text": "Live worship sessions."
        }]
    }, {
        "question":
        "How does the app encourage new believers to engage in community?",
        "answer_id":
        1,
        "options": [{
            "id": 0,
            "text": "By offering online games."
        }, {
            "id": 1,
            "text": "By connecting them with mentors and small groups."
        }, {
            "id": 2,
            "text": "By providing fitness challenges."
        }, {
            "id": 3,
            "text": "By offering cooking classes."
        }, {
            "id": 4,
            "text": "By promoting financial planning sessions."
        }]
    }, {
        "question":
        "What type of content is included in the app's learning paths?",
        "answer_id":
        0,
        "options": [{
            "id":
            0,
            "text":
            "Progressive modules on Christian doctrines and practices."
        }, {
            "id": 1,
            "text": "Daily news updates."
        }, {
            "id": 2,
            "text": "Professional development courses."
        }, {
            "id": 3,
            "text": "Travel guides for holy sites."
        }, {
            "id": 4,
            "text": "Language learning resources."
        }]
    }, {
        "question":
        "How does the app help new believers celebrate their spiritual milestones?",
        "answer_id":
        4,
        "options": [{
            "id": 0,
            "text": "By awarding cash prizes."
        }, {
            "id": 1,
            "text": "By organizing concerts."
        }, {
            "id": 2,
            "text": "By sending weekly inspirational emails."
        }, {
            "id": 3,
            "text": "By offering discounts on religious books."
        }, {
            "id":
            4,
            "text":
            "By recognizing milestones like spiritual birthdays with special content."
        }]
    }]
    return json_list


if __name__ == "__main__":
    print("Starting webserver...")
    # scheduler.start()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", '8000')),
        log_level=os.getenv('LOG_LEVEL', "info"),
        proxy_headers=True)
    # scheduler.shutdown()
