from fastapi import APIRouter, HTTPException, Depends
from typing import *
from uuid import uuid4
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.MyKind import *
from database import Base, engine, get_session
from db_models import Apps, Status

router = APIRouter(
    prefix="/MyKind",
    tags=["MyKind"]
)

@router.post("")
def create(item: MyKind, db: Session = Depends(get_session)):
    try:
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
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))
    return {"status": "success"}


@router.put("/uuid/specification")
def update_specification(uuid, specification: Dict[str, Any],  db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).get(uuid)
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        updated_json = obj.json.copy()
        updated_json['configuration']['specification'] = specification

        stmt = update(Apps).where(Apps.UUID == uuid).values(json=updated_json)
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))

    return {"status": "success"}

@router.put("/uuid/settings")
def update_settings(uuid, settings: Dict[str, Any], db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).get(uuid)
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        updated_json = obj.json.copy()
        updated_json['configuration']['settings'] = settings

        stmt = update(Apps).where(Apps.UUID == uuid).values(json=updated_json)
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))

    return {"status": "success"}


@router.put("/uuid/state")
def update_state(uuid, state: Status, db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).get(uuid)
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        stmt = update(Apps).where(Apps.UUID == uuid).values(state=state)
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))

    return {"status": "success"}


@router.delete("/uuid")
def delete(uuid,db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).get(uuid)
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        db.delete(obj)
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных")
    return {"status": "success"}


@router.get("/uuid",)
def read(uuid, db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).get(uuid)
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

    return {"status": "success",
            "data": obj}


@router.get("/uuid/state")
def read_state(uuid, db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).get(uuid)
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

    return {
        "status": "success",
        "data": {
            "state": obj.state
        }
    }
