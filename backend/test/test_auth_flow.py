"""
Fluxo de teste:
- cria usuário
- cria lead associado ao usuário
- faz login (recebe access_token e refresh_token)
- usa access_token para rota GET protegida
- usa refresh_token em /user/refresh para obter novo access_token
- usa novo access_token para rota POST protegida (`/user/intesao`)

Execute com o servidor rodando em http://localhost:8000
"""

import requests
import sys
import time

BASE = "http://localhost:8000"

user_data = {
    "name": "Test User",
    "numero": "999999999",
    "email": "user@example.com",
    "senha": "123",
}

lead_data = {
    "conversa_id": 111,
    "name": "Lead Test",
    "numero_lead": "lead123",
    "numero_user": user_data["numero"],
    "categoria": "MEDIA",
    "status": "PENDENTE",
    "resumo_conversa": "teste",
    "intencao": "compra",
    "data_hora_servico": "2026-06-16",
    "satisfacao": 0,
}


def pretty(resp):
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text


def main():
    print("1) Criando usuário...")
    r = requests.post(f"{BASE}/user/cadastro", json=user_data)
    print(pretty(r))
    if r.status_code not in (200, 201):
        # se já existir, seguir em frente
        print(
            "A criação do usuário pode ter falhado mas vamos prosseguir (verifique se já existe):",
            r.status_code,
        )

    time.sleep(0.5)

    print("\n2) Fazendo login para obter tokens (JSON /user/login)...")
    r = requests.post(
        f"{BASE}/user/login",
        json={"email": user_data["email"], "senha": user_data["senha"]},
    )
    status, body = pretty(r)
    print(status, body)
    if status != 200:
        print("Login falhou — verifique credenciais e servidor.")
        sys.exit(1)

    access = body.get("access_token")
    refresh = body.get("refresh_token")
    if not access or not refresh:
        print("Resposta de login não contém tokens completos. Resposta:", body)
        sys.exit(1)

    print("Access token obtido (size):", len(access))
    print("Refresh token obtido (size):", len(refresh))

    time.sleep(0.5)

    print(
        "\n3) Setando lista de intencao para o usuário (POST /user/intesao) usando access_token..."
    )
    headers = {"Authorization": f"Bearer {access}", "Content-Type": "application/json"}
    r = requests.post(
        f"{BASE}/user/intesao", json={"intencao": "compra"}, headers=headers
    )
    print(pretty(r))

    time.sleep(0.5)

    print("\n4) Criando lead associado ao usuário (depois de intencao setada)...")
    r = requests.post(f"{BASE}/leads/chat-lead", json=lead_data)
    print(pretty(r))
    if r.status_code >= 400 and r.status_code != 400:
        print("Erro ao criar lead; verifique o servidor e schemas.")

    time.sleep(0.5)

    print("\n5) Acessando rota GET protegida `/user/list-leads` com access_token...")
    headers = {"Authorization": f"Bearer {access}"}
    r = requests.get(f"{BASE}/user/list-leads", headers=headers)
    print(pretty(r))

    print(
        "\n5) Usando refresh_token em `/user/refresh` para obter novo access_token..."
    )
    headers = {"Authorization": f"Bearer {refresh}"}
    r = requests.get(f"{BASE}/user/refresh", headers=headers)
    status, body = pretty(r)
    print(status, body)
    if status != 200:
        print(
            "Refresh falhou — verifique se `/user/refresh` está protegido por token e se o refresh_token é válido."
        )
        sys.exit(1)

    new_access = body.get("access_token")
    if not new_access:
        print("/user/refresh não retornou novo access_token. Resposta:", body)
        sys.exit(1)

    print("Novo access token obtido (size):", len(new_access))

    time.sleep(0.5)

    print(
        "\n6) Usando novo access_token para rota POST protegida `/user/intesao` (setar intenção)"
    )
    headers = {
        "Authorization": f"Bearer {new_access}",
        "Content-Type": "application/json",
    }
    r = requests.post(
        f"{BASE}/user/intesao", json={"intencao": "compra"}, headers=headers
    )
    print(pretty(r))

    print("\nTeste finalizado.")


if __name__ == "__main__":
    main()
