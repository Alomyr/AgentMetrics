from dns import query
from fastapi import Depends, HTTPException
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

def normalize_intencao_value(value):
    if value is None:
        return None
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    if isinstance(value, list):
        normalized = [
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        ]
        return ",".join(normalized) if normalized else None
    raise ValueError("intencao deve ser uma string ou lista de strings")


# def verificar_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     from jose import jwt, JWTError
#     from model.User import UserDB
#     from config import SECRET_KEY, ALGORITHM

#     try:
#         dict_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id_user = dict_info.get("sub")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Acesso negado")
#     user = db.query(UserDB).filter(UserDB.id == int(id_user)).first()
#     if not user:
#         raise HTTPException(status_code=400, detail="Usuário não existe")
#     return user
