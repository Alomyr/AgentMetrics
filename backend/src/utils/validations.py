from dns import query
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


def get_record(db: Session, model, filter_data: dict, retorn_obj: bool = False):
    """
    Realiza uma consulta genérica e dinâmica em um modelo ORM usando filtros por correspondência.

    Args:
        db (Session): Sessão ativa do banco de dados.
        model: Classe de modelo do SQLAlchemy (ex: UserDB).
        filter_data (dict): Dicionário contendo atributos e valores para filtragem (ex: {'id': 1}).
        retorn_obj (bool, optional): Se True, retorna o objeto encontrado. Se False, retorna
            apenas um booleano de existência. Padrão: False.

    Returns:
        Any | bool: O registro localizado no banco ou True/False dependendo de 'retorn_obj'.
    """
    for column_name, value in filter_data.items():
        # Monta os filtros de forma encadeada no objeto query
        column = getattr(model, column_name)
        query = db.query(model).filter(column == value)

    result = query.first()
    return result if retorn_obj else (result is not None)


def result_check(obj, mensagem="", codigo=200, is_check=True):
    """
    Avalia a presença de uma entidade e dispara exceções HTTP parametrizadas de forma condicional.

    Args:
        obj (Any): Objeto ou registro inspecionado.
        mensagem (str, optional): Mensagem de erro inserida no detalhe da exceção.
        codigo (int, optional): Código de status HTTP lançado. Padrão: 200.
        is_check (bool, optional): Se True, lança erro se o objeto existir. Se False, lança
            erro caso o objeto seja nulo/falso. Padrão: True.

    Raises:
        HTTPException: Erro HTTP customizado se a condição disparar.
    """
    if is_check == True:
        if obj:
            raise HTTPException(status_code=codigo, detail=mensagem)
    else:
        if not obj:
            raise HTTPException(status_code=codigo, detail=mensagem)


def insert_db(db: Session, object, refresh=False):
    """
    Persiste um objeto na base de dados gerenciando transações e reversões automáticas.

    Args:
        db (Session): Sessão ativa do banco de dados.
        object (Any): Instância do modelo ORM a ser salva.
        refresh (bool, optional): Se True, sincroniza o estado do objeto com o banco. Padrão: False.

    Raises:
        HTTPException: Erro 500 caso ocorra uma falha de banco de dados (com Rollback aplicado).
    """
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
    """
    Normaliza e limpa estruturas brutas de intenções recebidas via requisições de clientes.

    Args:
        value (str | list | None): Valor vindo do payload.

    Returns:
        str | None: String contendo os valores limpos unidos por vírgulas ou None se vazio.

    Raises:
        ValueError: Caso o formato fornecido não seja string ou lista de strings.
    """
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
