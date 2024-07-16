from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from models.MyKind import MyKind
from database import Base, engine, get_session

router = APIRouter(
    prefix="/MyKind",
    tags=["MyKind"]
)

# POST: /{model_name}/
@router.post("")
def create(item: MyKind, db: Session = Depends(get_session)):
    # TODO добавление item в базу данных с дополнительными полями из БД
    return True


# PUT: /{model_name}/{{uuid}}/{{configuration}}/
@router.put("/uuid/configuration")
def update_configuration(uuid: UUID, configuration: dict,  db: Session = Depends(get_session)):
    pass

# PUT: /{model_name}/{{uuid}}/settings/
@router.put("/uuid/settings")
def update_settings(db: Session = Depends(get_session)):
    pass


# PUT: /{model_name}/{{uuid}}/state
@router.put("/uuid/state")
def update_state(uuid: UUID, state: dict, db: Session = Depends(get_session)):
    pass


# DELETE: /{model_name}/{{uuid}}/
@router.delete("/uuid")
def delete(uuid: UUID,db: Session = Depends(get_session)):
    pass


# GET: /{model_name}/{{uuid}}
@router.get("/uuid",)
def read(uuid: UUID, db: Session = Depends(get_session)):
    pass


# GET: /{model_name}/{{uuid}}/state
@router.get("/uuid/state")
def read_state(uuid: UUID, db: Session = Depends(get_session)):
    pass
