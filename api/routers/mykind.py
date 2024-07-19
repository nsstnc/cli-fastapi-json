from fastapi import APIRouter, HTTPException, Depends
from typing import *
from uuid import uuid4
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from api.models.mykind import *
from api.database import Base, engine, get_session
from api.db_models import Apps, Status
from api.rabbitmq import *
import json

router = APIRouter(
    prefix="/mykind",
    tags=["mykind"]
)

@router.post("")
def create(item: mykind, db: Session = Depends(get_session)):
    try:
        jsn = item.dict()
        if jsn['kind'] != "mykind":
            raise HTTPException(status_code=400, detail="Неподходящий тип документа (kind)")
        values = {
            'UUID': str(uuid4()),
            'kind': jsn['kind'],
            'name': jsn['name'],
            'version': jsn['version'],
            'description': jsn['description'],
            'state': Status.new,
            'json': jsn
        }

        stmt = insert(Apps).values(values)
        db.execute(stmt)
        db.commit()

        try:
            values['state'] = str(values['state'])
            send_message_rabbit(json.dumps(values))
        except Exception as e:
            raise HTTPException(status_code=200, detail="Не удалось отправить сообщение в брокер" + str(e))



    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))
    return {"status": "success"}


@router.put("/{uuid}/specification")
def update_specification(uuid: str, specification: Dict[str, Any], db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).filter(Apps.UUID == uuid, Apps.kind == "mykind").first()
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        updated_json = obj.json.copy()
        updated_json['configuration']['specification'] = specification

        stmt = update(Apps).where(Apps.UUID == uuid).values(json=updated_json)
        db.execute(stmt)
        db.commit()


        try:
            send_message_rabbit(json.dumps({"message": f"{uuid} specification updated successfully"}))
        except Exception as e:
            raise HTTPException(status_code=200, detail="Не удалось отправить сообщение в брокер" + str(e))


    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))

    return {"status": "success"}

@router.put("/{uuid}/settings")
def update_settings(uuid: str, settings: Dict[str, Any], db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).filter(Apps.UUID == uuid, Apps.kind == "mykind").first()
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        updated_json = obj.json.copy()
        updated_json['configuration']['settings'] = settings

        stmt = update(Apps).where(Apps.UUID == uuid).values(json=updated_json)
        db.execute(stmt)
        db.commit()

        try:
            send_message_rabbit(json.dumps({"message": f"{uuid} settings updated successfully"}))
        except Exception as e:
            raise HTTPException(status_code=200, detail="Не удалось отправить сообщение в брокер" + str(e))



    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))

    return {"status": "success"}


@router.put("/{uuid}/state")
def update_state(uuid: str, state: Status, db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).filter(Apps.UUID == uuid, Apps.kind == "mykind").first()
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        stmt = update(Apps).where(Apps.UUID == uuid).values(state=state)
        db.execute(stmt)
        db.commit()

        try:
            send_message_rabbit(json.dumps({"message": f"{uuid} state updated successfully"}))
        except Exception as e:
            raise HTTPException(status_code=200, detail="Не удалось отправить сообщение в брокер" + str(e))



    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка базы данных: " + str(e))

    return {"status": "success"}


@router.delete("/{uuid}")
def delete(uuid: str, db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).filter(Apps.UUID == uuid, Apps.kind == "mykind").first()
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        db.delete(obj)
        db.commit()

        try:
            send_message_rabbit(json.dumps({"message": f"{uuid} deleted successfully"}))
        except Exception as e:
            raise HTTPException(status_code=200, detail="Не удалось отправить сообщение в брокер" + str(e))


    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных")
    return {"status": "success"}


@router.get("/{uuid}")
def read(uuid: str, db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).filter(Apps.UUID == uuid, Apps.kind == "mykind").first()
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

    return {"status": "success",
            "data": obj}


@router.get("/{uuid}/state")
def read_state(uuid: str, db: Session = Depends(get_session)):
    try:
        obj = db.query(Apps).filter(Apps.UUID == uuid, Apps.kind == "mykind").first()
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