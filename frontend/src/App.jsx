import { useState, useEffect } from "react";
import Register from "./components/Register";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [page, setPage] = useState("register");
  const [message, setMessage] = useState("");
  const [feedback, setFeedback] = useState([]);

  // if tokens are already saved, go straight to the dashboard
  useEffect(() => {
    if (localStorage.getItem("access_token")) {
      setPage("dashboard");
      loadFeedback();
    }
  }, []);

  function showPage(name) {
    setMessage("");
    setPage(name);
  }

  // POST /register   (A1)
  function register(username, email, password) {
    fetch(API_URL + "/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, email: email, password: password }),
    })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data: data })))
      .then((result) => {
        if (!result.ok) {
          setMessage("Error: " + JSON.stringify(result.data.detail));
          return;
        }
        setPage("login");                                   // success -> go to login
        setMessage("Registered successfully, please log in");
      });
  }

  // POST /login   (A2)
  function login(email, password) {
    fetch(API_URL + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, password: password }),
    })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data: data })))
      .then((result) => {
        if (!result.ok) {
          setMessage("Error: " + JSON.stringify(result.data.detail));
          return;
        }
        localStorage.setItem("access_token", result.data.access_token);
        localStorage.setItem("refresh_token", result.data.refresh_token);
        showPage("dashboard");
        loadFeedback();                                     // fetch feedback right after login
      });
  }

  // GET /feedback   (E1) - if the access token expired, refresh it once and try again
  function loadFeedback(retried) {
    fetch(API_URL + "/feedback", {
      headers: { token: localStorage.getItem("access_token") },
    })
      .then((response) => response.json().then((data) => ({ status: response.status, data: data })))
      .then((result) => {
        if (result.status === 401 && !retried) {
          refresh();
          return;
        }
        if (result.status !== 200) {
          setMessage("Error: " + JSON.stringify(result.data.detail));
          return;
        }
        setFeedback(result.data);
      });
  }

  // POST /refresh   (A3) - get a new access token using the refresh token
  function refresh() {
    fetch(API_URL + "/refresh", {
      method: "POST",
      headers: { "refresh-token": localStorage.getItem("refresh_token") },
    })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data: data })))
      .then((result) => {
        if (!result.ok) {
          logout();                                         // refresh token also expired
          setMessage("Session expired, please log in again");
          return;
        }
        localStorage.setItem("access_token", result.data.access_token);
        loadFeedback(true);
      });
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setFeedback([]);
    showPage("login");
  }

  return (
    <>
      <h1>Feedback Manager</h1>
      {message !== "" ? <p>{message}</p> : null}

      {page === "register" ? <Register onRegister={register} onGoLogin={() => showPage("login")} /> : null}
      {page === "login" ? <Login onLogin={login} onGoRegister={() => showPage("register")} /> : null}
      {page === "dashboard" ? <Dashboard feedback={feedback} onLogout={logout} /> : null}
    </>
  );
}

export default App;
