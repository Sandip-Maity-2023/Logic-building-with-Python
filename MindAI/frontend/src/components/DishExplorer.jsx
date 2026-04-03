import React, { useMemo, useState } from "react";

function DishExplorer({ dishes, onSubmit, isLoading }) {
  const [dish, setDish] = useState("");
  const [latitude, setLatitude] = useState(28.61);
  const [longitude, setLongitude] = useState(77.2);
  const [message, setMessage] = useState("");

  const cuisines = useMemo(
    () => [...new Set(dishes.map((item) => item.cuisine))],
    [dishes],
  );

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!dish) {
      setMessage("Choose a dish to unlock restaurant recommendations.");
      return;
    }

    setMessage("");
    await onSubmit({ dish, latitude: Number(latitude), longitude: Number(longitude) });
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">Dish Explorer</span>
          <h3>Browse by exact craving</h3>
        </div>
        <p>
          Pick a dish from any old MoodieFoodie category and rank matching
          restaurants by quality, value, and distance.
        </p>
      </div>

      <div className="helper-grid compact-grid">
        {cuisines.map((cuisine) => (
          <div key={cuisine} className="helper-card">
            <span>Cuisine</span>
            <strong>{cuisine}</strong>
          </div>
        ))}
      </div>

      <form className="panel-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>Dish</span>
          <select value={dish} onChange={(event) => setDish(event.target.value)}>
            <option value="">Select a dish</option>
            {dishes.map((item) => (
              <option key={item.slug} value={item.slug}>
                {item.label} · {item.cuisine}
              </option>
            ))}
          </select>
        </label>

        <div className="field-row">
          <label className="field">
            <span>Latitude</span>
            <input
              type="number"
              step="0.01"
              value={latitude}
              onChange={(event) => setLatitude(event.target.value)}
            />
          </label>
          <label className="field">
            <span>Longitude</span>
            <input
              type="number"
              step="0.01"
              value={longitude}
              onChange={(event) => setLongitude(event.target.value)}
            />
          </label>
        </div>

        {message ? <div className="inline-message">{message}</div> : null}

        <div className="panel-actions">
          <button type="submit" className="primary-button" disabled={isLoading}>
            {isLoading ? "Ranking..." : "Find restaurants"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default DishExplorer;
