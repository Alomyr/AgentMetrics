from pydantic import BaseModel

class login_root(BaseModel):
    login: str
    senha: str
