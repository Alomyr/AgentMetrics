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


def result_check(obj, mensagem="", codigo=200, is_check=True):

    if is_check == True:
        if obj:
            raise HTTPException(status_code=codigo, detail=mensagem)
    else:
        if not obj:
            raise HTTPException(status_code=codigo, detail=mensagem)


def insert_db(db: Session, object, refresh=False):
    try:
        db.add(object)
        db.commit()
        if refresh:
            db.refresh(object)
    except Exception as e:
        db.rollback()
        # Imprima o erro real para saber o que está acontecendo no banco
        print(f"ERRO DO SQLALCHEMY: {e}")
        raise HTTPException(status_code=500, detail=str(e))
