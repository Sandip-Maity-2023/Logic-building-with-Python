import React, { useState } from "react";

const cuisineSuggestions = [
  "Indian",
  "Italian",
  "Chinese",
  "Mexican",
  "Thai",
  "Continental",
  "Cafe",
  "Street Food",
];

const presets = [
  { label: "Balanced", cuisine: "Indian", rating: 4.2, sentiment: 0.74 },
  { label: "Premium", cuisine: "Italian", rating: 4.7, sentiment: 0.88 },
  { label: "Buzzing", cuisine: "Cafe", rating: 4.1, sentiment: 0.91 },
];

function ManualInput({ onSubmit, isLoading }) {
  const [form, setForm] = useState({
    cuisine: "",
    rating: 4.2,
    sentiment: 0.75,
  });
  const [message, setMessage] = useState("");

  const updateField = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }));
  };

  const applyPreset = (preset) => {
    setForm({
      cuisine: preset.cuisine,
      rating: preset.rating,
      sentiment: preset.sentiment,
    });
    setMessage(`Preset "${preset.label}" applied.`);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!form.cuisine.trim()) {
      setMessage("Choose a cuisine before generating recommendations.");
      return;
    }

    setMessage("");
    await onSubmit({
      cuisine: form.cuisine.trim(),
      rating: Number(form.rating),
      sentiment: Number(form.sentiment),
    });
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">Manual scenario</span>
          <h3>Simulate one preference profile</h3>
        </div>
        <p>Dial in the exact cuisine, rating, and sentiment blend you want the model to prioritize.</p>
      </div>

      <div className="preset-row">
        {presets.map((preset) => (
          <button
            key={preset.label}
            type="button"
            className="chip-button"
            onClick={() => applyPreset(preset)}
          >
            {preset.label}
          </button>
        ))}
      </div>

      <form className="panel-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>Cuisine focus</span>
          <input
            list="cuisine-options"
            value={form.cuisine}
            placeholder="Try Indian, Cafe, Italian..."
            onChange={(event) => updateField("cuisine", event.target.value)}
          />
          <datalist id="cuisine-options">
            {cuisineSuggestions.map((item) => (
              <option key={item} value={item} />
            ))}
          </datalist>
        </label>

        <label className="field">
          <div className="field-topline">
            <span>Minimum rating</span>
            <strong>{Number(form.rating).toFixed(1)}</strong>
          </div>
          <input
            type="range"
            min="1"
            max="5"
            step="0.1"
            value={form.rating}
            onChange={(event) => updateField("rating", event.target.value)}
          />
        </label>

        <label className="field">
          <div className="field-topline">
            <span>Sentiment score</span>
            <strong>{Number(form.sentiment).toFixed(2)}</strong>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={form.sentiment}
            onChange={(event) => updateField("sentiment", event.target.value)}
          />
        </label>

        {message ? <div className="inline-message">{message}</div> : null}

        <div className="panel-actions">
          <button type="submit" className="primary-button" disabled={isLoading}>
            {isLoading ? "Generating..." : "Get recommendations"}
          </button>
          <button
            type="button"
            className="ghost-button"
            onClick={() => {
              setForm({ cuisine: "", rating: 4.2, sentiment: 0.75 });
              setMessage("");
            }}
          >
            Reset
          </button>
        </div>
      </form>
    </section>
  );
}

export default ManualInput;
