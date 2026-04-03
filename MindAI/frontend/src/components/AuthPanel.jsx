import React, { useState } from "react";

function AuthPanel({ session, onLogin, isLoading }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    setMessage("");

    try {
      await onLogin(mode, form);
      setMessage(mode === "login" ? "Welcome back." : "Account created.");
      setForm({ username: "", email: "", password: "" });
    } catch (error) {
      setMessage(
        error?.response?.data?.detail || "That request could not be completed.",
      );
    }
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">Account</span>
          <h3>Save your food profile</h3>
        </div>
        <p>
          Recreates MoodieFoodie sign-up and login flows so feedback and mood
          activity feel personal.
        </p>
      </div>

      <div className="segmented-control">
        <button
          type="button"
          className={mode === "login" ? "active" : ""}
          onClick={() => setMode("login")}
        >
          Login
        </button>
        <button
          type="button"
          className={mode === "signup" ? "active" : ""}
          onClick={() => setMode("signup")}
        >
          Sign up
        </button>
      </div>

      <form className="panel-form" onSubmit={submit}>
        {mode === "signup" ? (
          <label className="field">
            <span>Display name</span>
            <input
              value={form.username}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  username: event.target.value,
                }))
              }
              placeholder="Mindful foodie"
            />
          </label>
        ) : null}

        <label className="field">
          <span>Email</span>
          <input
            type="email"
            value={form.email}
            onChange={(event) =>
              setForm((current) => ({ ...current, email: event.target.value }))
            }
            placeholder="you@example.com"
          />
        </label>

        <label className="field">
          <span>Password</span>
          <input
            type="password"
            value={form.password}
            onChange={(event) =>
              setForm((current) => ({
                ...current,
                password: event.target.value,
              }))
            }
            placeholder="Minimum 6 characters"
          />
        </label>

        {message ? <div className="inline-message">{message}</div> : null}
        {session?.user ? (
          <div className="helper-card">
            <span>Signed in</span>
            <strong>{session.user.username}</strong>
          </div>
        ) : null}

        <div className="panel-actions">
          <button type="submit" className="primary-button" disabled={isLoading}>
            {isLoading ? "Working..." : mode === "login" ? "Login" : "Create account"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default AuthPanel;
