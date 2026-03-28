"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [todos, setTodos] = useState<string[]>([]);
  const [text, setText] = useState("");

  const fetchTodos = async () => {
    const res = await fetch("http://127.0.0.1:8000/todos");
    const data = await res.json();
    setTodos(data.map((t: any) => t.text));
  };

  const addTodo = async () => {
    await fetch("http://127.0.0.1:8000/todos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    setText("");
    fetchTodos();
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>Todo App</h1>

      <input
        placeholder="Enter a new todo"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={addTodo}>Add</button>

      <ul>
        {todos.map((todo, i) => (
          <li key={i}>{todo}</li>
        ))}
      </ul>
    </div>
  );
}