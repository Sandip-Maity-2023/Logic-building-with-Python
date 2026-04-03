import React, { useState } from "react";

function FeedbackStudio({
  restaurants,
  dishes,
  moods,
  token,
  onSubmit,
  isLoading,
}) {
  const [form, setForm] = useState({
    restaurant: "",
    food: "",
    mood: "",
    rating: 4,
  });
  const [message, setMessage] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    if (!form.restaurant || !form.food || !form.mood) {
      setMessage("Fill all feedback fields before submitting.");
      return;
    }

    const response = await onSubmit({ ...form, token, rating: Number(form.rating) });
    setMessage(response?.message || "Feedback saved.");
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">Feedback Loop</span>
          <h3>Train the experience with each order</h3>
        </div>
        <p>
          Ported from the old rating flow: submit the restaurant, food choice,
          mood, and score to keep recommendations fresh.
        </p>
      </div>

      <form className="panel-form" onSubmit={submit}>
        <label className="field">
          <span>Restaurant</span>
          <select
            value={form.restaurant}
            onChange={(event) =>
              setForm((current) => ({ ...current, restaurant: event.target.value }))
            }
          >
            <option value="">Choose a restaurant</option>
            {restaurants.map((item) => (
              <option key={item.name} value={item.name}>
                {item.name}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Food</span>
          <select
            value={form.food}
            onChange={(event) =>
              setForm((current) => ({ ...current, food: event.target.value }))
            }
          >
            <option value="">Choose a food item</option>
            {dishes.map((item) => (
              <option key={item.slug} value={item.label}>
                {item.label}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Mood</span>
          <select
            value={form.mood}
            onChange={(event) =>
              setForm((current) => ({ ...current, mood: event.target.value }))
            }
          >
            <option value="">Choose your mood</option>
            {moods.map((item) => (
              <option key={item.slug} value={item.slug}>
                {item.label}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <div className="field-topline">
            <span>Rating</span>
            <strong>{Number(form.rating).toFixed(1)}</strong>
          </div>
          <input
            type="range"
            min="0"
            max="5"
            step="0.1"
            value={form.rating}
            onChange={(event) =>
              setForm((current) => ({ ...current, rating: event.target.value }))
            }
          />
        </label>

        {message ? <div className="inline-message">{message}</div> : null}

        <div className="panel-actions">
          <button type="submit" className="primary-button" disabled={isLoading}>
            {isLoading ? "Saving..." : "Submit feedback"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default FeedbackStudio;
