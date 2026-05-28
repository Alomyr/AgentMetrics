from fastapi import APIRouter, Depends, HTTPException
from model.database import get_db
from sqlalchemy.orm import Session


def check_if_exists(db: Session, model, filter_name: str, data):

    column = getattr(model, filter_name)
    value = getattr(data, filter_name)
    is_exists = db.query(model).filter(column == value).first() is not None
    return is_exists


# colocar funções de reutilizadas aqui


def check_if_exists_login(db: Session, model, filter_name: str, data):

    column = getattr(model, filter_name)
    value = getattr(data, filter_name)
    is_exists = db.query(model).filter(column == value).first()
    return is_exists


# refatorar para ser uma função unica essas duas depois
