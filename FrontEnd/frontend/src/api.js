import axios from "axios";

const API_PREFIX = "/api";
const api = axios.create({
  baseURL: API_PREFIX,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function fetchUsers() {
  try {
    const response = await api.get("/user/list-user");
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message;
    throw new Error(`Erro ao buscar usuários: ${message}`);
  }
}

export async function loginUser(email, senha) {
  try {
    const response = await api.post("/user/login", { email, senha });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message;
    throw new Error(message || "Falha no login");
  }
}

export async function fetchWithToken(path, token, options = {}) {
  try {
    const response = await api({
      url: path,
      method: options.method || "get",
      headers: {
        Authorization: `Bearer ${token}`,
        ...options.headers,
      },
      data: options.body || options.data || null,
      params: options.params || null,
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message;
    throw new Error(
      message || error.response?.statusText || "Erro na requisição",
    );
  }
}
