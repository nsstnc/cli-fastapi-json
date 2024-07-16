from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import uuid4
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from models.MyKind import MyKind
from database import Base, engine, get_session
from db_models import Apps, Status

router = APIRouter(
    prefix="/MyKind",
    tags=["MyKind"]
)

# POST: /{model_name}/
@router.post("")
def create(item: MyKind, db: Session = Depends(get_session)):
    json = item.dict()
    values = {
        'UUID': str(uuid4()),
        'kind': json['kind'],
        'name': json['name'],
        'version': json['version'],
        'description': json['description'],
        'state': Status.new,
        'json': json
    }

    stmt = insert(Apps).values(values)
    db.execute(stmt)
    db.commit()
    return {"status": "success"}


# PUT: /{model_name}/{{uuid}}/{{configuration}}/
@router.put("/uuid/configuration")
def update_configuration(uuid, configuration: dict,  db: Session = Depends(get_session)):
    pass

# PUT: /{model_name}/{{uuid}}/settings/
@router.put("/uuid/settings")
def update_settings(db: Session = Depends(get_session)):
    pass


# PUT: /{model_name}/{{uuid}}/state
@router.put("/uuid/state")
def update_state(uuid, state: dict, db: Session = Depends(get_session)):
    pass


# DELETE: /{model_name}/{{uuid}}/
@router.delete("/uuid")
def delete(uuid,db: Session = Depends(get_session)):
    pass


# GET: /{model_name}/{{uuid}}
@router.get("/uuid",)
def read(uuid, db: Session = Depends(get_session)):
    pass


# GET: /{model_name}/{{uuid}}/state
@router.get("/uuid/state")
def read_state(uuid, db: Session = Depends(get_session)):
    pass
