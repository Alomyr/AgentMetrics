from dns import query
from fastapi import APIRouter, Depends, HTTPException
from model.database import get_db
from sqlalchemy.orm import Session

def get_record(db: Session, model, filter_data: dict, retorn_obj: bool = False):

    for column_name, value in filter_data.items():
        column = getattr(model, column_name)
        query = db.query(model).filter(column == value)

    result = query.first()
    return result if retorn_obj else (result is not None)
