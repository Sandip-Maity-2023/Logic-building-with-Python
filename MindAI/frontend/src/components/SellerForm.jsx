import React, { useState } from "react";

function SellerForm({ sellers, onSubmit, isLoading }) {
  const [form, setForm] = useState({ name: "", address: "", items: "" });
  const [message, setMessage] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    const response = await onSubmit(form);
    setMessage(response?.message || "Seller request submitted.");
    setForm({ name: "", address: "", items: "" });
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">Seller Network</span>
          <h3>Let small food businesses sell through MindAI</h3>
        </div>
        <p>
          This brings over the MoodieFoodie seller onboarding path for tea
          shops, homemade dessert makers, and local specialty kitchens.
        </p>
      </div>

      <div className="helper-grid">
        <div className="helper-card">
          <span>Registered sellers</span>
          <strong>{sellers.length}</strong>
        </div>
        <div className="helper-card">
          <span>Popular use case</span>
          <strong>Tea, juices, chocolates</strong>
        </div>
      </div>

      <form className="panel-form" onSubmit={submit}>
        <label className="field">
          <span>Name</span>
          <input
            value={form.name}
            onChange={(event) =>
              setForm((current) => ({ ...current, name: event.target.value }))
            }
            placeholder="Your business name"
          />
        </label>
        <label className="field">
          <span>Address</span>
          <input
            value={form.address}
            onChange={(event) =>
              setForm((current) => ({ ...current, address: event.target.value }))
            }
            placeholder="City, locality, landmark"
          />
        </label>
        <label className="field">
          <span>Items</span>
          <textarea
            rows="3"
            value={form.items}
            onChange={(event) =>
              setForm((current) => ({ ...current, items: event.target.value }))
            }
            placeholder="Tea, brownies, sandwiches..."
          />
        </label>

        {message ? <div className="inline-message">{message}</div> : null}

        <div className="panel-actions">
          <button type="submit" className="primary-button" disabled={isLoading}>
            {isLoading ? "Submitting..." : "Become a seller"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default SellerForm;
