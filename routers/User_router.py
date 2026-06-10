from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.database import get_db
from model.security import get_password_hash, verify_password
from routers.dependencies import get_record, result_check, insert_db
from model.User import UserDB
from model.schemas import Creat_new_user, edit_user, login_user, intenso
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

user_routers = APIRouter(prefix="/user", tags=["User"])


# tem q permitir a promoção de lead para user avaliar


@user_routers.get("/list-user")
def listar_user(db: Session = Depends(get_db)):
    # Aqui lógica de consulta ao banco
    return {"mensagem": "Lista de usuarios"}


@user_routers.post("/cadastro")
def add_new_user(user_data: Creat_new_user, db: Session = Depends(get_db)):
    existing_user = get_record(db, UserDB, {"email": user_data.email}, True)
    result_check(existing_user, "O email já está cadastrado.", 404)

    existing_user_numero = get_record(db, UserDB, {"numero": user_data.numero}, True)
    result_check(existing_user_numero, "O Numero já está cadastrado.", 404)

    novo_user = UserDB(
        name=user_data.name,
        numero=user_data.numero,
        email=user_data.email,
        senha=get_password_hash(user_data.senha),
    )
    insert_db(db, novo_user, True)
    return {"message": "Sucesso", "user_id": novo_user.id}


# Refatorar os metodos de edição do user,
# adicionar uma tablea de metricas no user,
@user_routers.post("/nova-senha")
def edit_password(dados: edit_user, db: Session = Depends(get_db)):
    user = get_record(db, UserDB, {"numero": dados.numero}, True)
    if user:
        user_update = db.query(UserDB).filter(UserDB.id == user.id).first()
        if user_update:
            user_update.senha = get_password_hash(dados.nova_senha)
            db.commit()
            db.refresh(user)
    return {
        "message": "Pareamento senha atualizado com sucesso",
        "User:": user.id,
    }


@user_routers.post("/nova-senha")
def edit_password(dados: edit_user, db: Session = Depends(get_db)):
    user = get_record(db, UserDB, {"email": dados.email}, True)
    if user:
        user_update = db.query(UserDB).filter(UserDB.id == user.id).first()
        if user_update:
            user_update.senha = get_password_hash(dados.nova_senha)
            db.commit()
            db.refresh(user)
    return {
        "message": "Pareamento senha atualizado com sucesso",
        "User:": user.id,
    }


@user_routers.post("/novo-email")
def edit_email(dados: edit_user, db: Session = Depends(get_db)):
    user = get_record(db, UserDB, {"numero": dados.numero}, True)
    if user:
        user_update = db.query(UserDB).filter(UserDB.id == user.id).first()
        if user_update:
            user_update.email = dados.email
            db.commit()
            db.refresh(user)
    return {
        "message": "Pareamento email atualizado com sucesso",
        "User:": user.id,
    }


@user_routers.post("/novo-numero")
def edit_numero(dados: edit_user, db: Session = Depends(get_db)):
    user = get_record(db, UserDB, {"email": dados.email}, True)
    if user:
        user_update = db.query(UserDB).filter(UserDB.id == user.id).first()
        if user_update:
            user_update.numero = dados.numero
            db.commit()
            db.refresh(user)
    return {
        "message": "Pareamento numero atualizado com sucesso",
        "User:": user.id,
    }


@user_routers.post("/novo-nome")
def edit_nome(dados: edit_user, db: Session = Depends(get_db)):
    user = get_record(db, UserDB, {"email": dados.email}, True)
    if user:
        user_update = db.query(UserDB).filter(UserDB.id == user.id).first()
        if user_update:
            user_update.nome = dados.nome
            db.commit()
            db.refresh(user)
    return {
        "message": "Pareamento nome atualizado com sucesso",
        "User:": user.id,
    }


def token(user_id, duracao=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao
    dic_info = {"sub": user_id, "exp": data_expiracao}
    token = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return token


@user_routers.post("/validar-user")
def validar_user(login: login_user, db: Session = Depends(get_db)):

    user = get_record(db, UserDB, {"email": login.email}, True)

    result_check(user, "Senha ou Login errados", 400, False)

    if not verify_password(login.senha, user.senha):
        raise HTTPException(status_code=400, detail="Senha ou Login errados")
    else:
        access_token = token(user.id)
        refresh_token = token(user.id, timedelta(days=1))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "message": "Autenticação bem-sucedida",
        }


def serialize_intencao(value):
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
    raise HTTPException(
        status_code=400, detail="intencao deve ser uma string ou lista de strings"
    )


@user_routers.post("/intesao")
def def_intesao(data_user: intenso, db: Session = Depends(get_db)):

    user_intesao = get_record(db, UserDB, {"numero": data_user.numero}, True)

    if user_intesao:
        user_update = db.query(UserDB).filter(UserDB.id == user_intesao.id).first()
        if user_update:
            user_update.intencao = serialize_intencao(data_user.intencao)
            db.commit()
            db.refresh(user_intesao)
    return {
        "message": "Pareamento intensao atualizado com sucesso",
        "User:": user_intesao.id,
    }
