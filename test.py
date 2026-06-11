"""
Script para testar a validade do token JWT
"""

from jose import jwt, JWTError
from datetime import datetime, timezone
from config import SECRET_KEY, ALGORITHM
import requests

header = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzgxMjc0OTExfQ.J5f1XK7Mw2WfdBEhlHsleBhDzX-39eVcdx122kqPapg"
}
requisisao = requests.get("http://127.0.0.1:8000/user/refresh", headers=header)
print(requisisao)
print(requisisao.json)

def decodificar_token(token: str) -> dict:
    """
    Decodifica e valida um token JWT

    Args:
        token: Token JWT em string

    Returns:
        dict com os dados do token ou None se inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✓ Token decodificado com sucesso!")
        print(f"  Conteúdo: {payload}")
        return payload
    except JWTError as e:
        print(f"✗ Erro ao decodificar token: {e}")
        return None


def validar_token(token: str) -> bool:
    """
    Valida se o token é válido e não expirou

    Args:
        token: Token JWT em string

    Returns:
        True se válido, False caso contrário
    """
    payload = decodificar_token(token)

    if not payload:
        return False

    # Verificar expiração
    exp = payload.get("exp")
    if exp:
        tempo_atual = datetime.now(timezone.utc).timestamp()
        if exp < tempo_atual:
            print(
                f"✗ Token expirado! Expiração: {datetime.fromtimestamp(exp, tz=timezone.utc)}"
            )
            print(
                f"  Tempo atual: {datetime.fromtimestamp(tempo_atual, tz=timezone.utc)}"
            )
            return False
        else:
            print(
                f"✓ Token não expirou. Válido até: {datetime.fromtimestamp(exp, tz=timezone.utc)}"
            )

    # Verificar presença de 'sub' (user_id)
    sub = payload.get("sub")
    if not sub:
        print("✗ Token não contém 'sub' (user_id)")
        return False

    print(f"✓ ID do usuário no token: {sub}")
    return True


def testar_token_fornecido():
    """
    Testa o token fornecido pelo usuário
    """
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzgxMjc0OTExfQ.J5f1XK7Mw2WfdBEhlHsleBhDzX-39eVcdx122kqPapg"

    print("=" * 60)
    print("TESTE DE VALIDAÇÃO DE TOKEN JWT")
    print("=" * 60)
    print(f"\nToken testado:\n{token}\n")

    resultado = validar_token(token)

    print("\n" + "=" * 60)
    if resultado:
        print("RESULTADO: ✓ TOKEN VÁLIDO")
    else:
        print("RESULTADO: ✗ TOKEN INVÁLIDO")
    print("=" * 60)


def testar_multiplos_tokens():
    """
    Permite testar múltiplos tokens
    """
    print("=" * 60)
    print("TESTE INTERATIVO DE TOKENS")
    print("=" * 60)

    while True:
        token = input("\nCole o token (ou 'sair' para finalizar):\n> ").strip()

        if token.lower() == "sair":
            print("Encerrando...")
            break

        if not token:
            print("Token vazio! Tente novamente.")
            continue

        print()
        validar_token(token)
        print()


if __name__ == "__main__":
    import sys

    print("Modo de execução:")
    print("1. Testar token fornecido (padrão)")
    print("2. Testar múltiplos tokens (interativo)")
    print()

    # Se executar sem argumentos, testa o token fornecido
    # Se executar com 'interativo', ativa o modo interativo
    if len(sys.argv) > 1 and sys.argv[1] == "interativo":
        testar_multiplos_tokens()
    else:
        testar_token_fornecido()
