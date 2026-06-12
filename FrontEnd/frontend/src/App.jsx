import { useEffect, useState } from "react";
import "./App.css";
import { fetchUsers, loginUser } from "./api";

function App() {
  const [users, setUsers] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [token, setToken] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchUsers()
      .then((data) => setUsers(data))
      .catch((err) => setError(err.message || "Erro ao carregar usuários"))
      .finally(() => setLoading(false));
  }, []);

  const handleLogin = async (event) => {
    event.preventDefault();
    setError(null);

    try {
      const data = await loginUser(email, senha);
      setToken(data.access_token);
    } catch (err) {
      setError(err.message || "Falha no login");
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Consumo FastAPI</h1>
        <p>
          API: <code>http://127.0.0.1:8000</code> via proxy Vite em{" "}
          <code>/api</code>
        </p>
      </header>

      <section>
        <h2>Usuários</h2>
        {loading && <p>Carregando...</p>}
        {error && <p className="error">{error}</p>}
        {!loading && users && <pre>{JSON.stringify(users, null, 2)}</pre>}
      </section>

      <section>
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>

          <label>
            Senha
            <input
              type="password"
              value={senha}
              onChange={(event) => setSenha(event.target.value)}
              required
            />
          </label>

          <button type="submit">Entrar</button>
        </form>
        {token && (
          <div>
            <h3>Token Bearer</h3>
            <textarea readOnly value={token} rows={3} />
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
