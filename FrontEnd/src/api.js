import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function fetchUsers() {
  const response = await api.get("/user/list-user");
  return response.data;
}

export async function loginUser(email, senha) {
  const response = await api.post("/user/login", { email, senha });
  return response.data;
}

export async function fetchWithToken(path, token, options = {}) {
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
}
