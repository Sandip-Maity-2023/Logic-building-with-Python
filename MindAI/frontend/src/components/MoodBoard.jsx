import React from "react";

function MoodBoard({ moods, activeMood, recommendations, onPick, isLoading }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">Mood Engine</span>
          <h3>Choose what to eat by how you feel</h3>
        </div>
        <p>
          The signature MoodieFoodie idea now lives inside MindAI as a dedicated
          mood-driven suggestion board.
        </p>
      </div>

      <div className="mood-grid">
        {moods.map((item) => (
          <button
            key={item.slug}
            type="button"
            className={`mood-pill${activeMood === item.slug ? " active" : ""}`}
            onClick={() => onPick(item.slug)}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="mood-results">
        {isLoading ? (
          <div className="inline-message">Loading mood recommendations...</div>
        ) : recommendations.length ? (
          recommendations.map((item, index) => (
            <article className="history-card" key={`${item.dish}-${index}`}>
              <span>{item.cuisine}</span>
              <strong>{item.dish}</strong>
              <p>Preference score: {item.score}</p>
            </article>
          ))
        ) : (
          <div className="inline-message">
            Select a mood to see dishes that fit the moment.
          </div>
        )}
      </div>
    </section>
  );
}

export default MoodBoard;
