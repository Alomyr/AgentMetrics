from pydantic import BaseModel


class login_root(BaseModel):
    """
    Schema de validação para dados de login de administradores.

    Utilizado no corpo das requisições de autenticação para garantir
    que as credenciais fornecidas estejam no formato correto antes
    de processar a lógica de negócios.

    Attributes:
        login (str): Nome de usuário do administrador.
        senha (str): Senha em texto limpo enviada para verificação.
    """

    login: str
    senha: str
