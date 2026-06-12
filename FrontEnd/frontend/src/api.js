const API_PREFIX = "/api";

export async function fetchUsers() {
  const response = await fetch(`${API_PREFIX}/user/list-user`);
  if (!response.ok) {
    throw new Error(`Erro ao buscar usuários: ${response.statusText}`);
  }
  return response.json();
}

export async function loginUser(email, senha) {
  const response = await fetch(`${API_PREFIX}/user/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, senha }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Falha no login");
  }

  return response.json();
}

export async function fetchWithToken(path, token, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
    ...options.headers,
  };

  const response = await fetch(`${API_PREFIX}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || response.statusText);
  }

  return response.json();
}
