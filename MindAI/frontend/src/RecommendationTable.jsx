import React, { useMemo, useState } from "react";

const downloadFile = (content, filename, type) => {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
};

const getSentiment = (item) => Number(item.sentiment_score ?? item.sentiment) || 0;

function RecommendationTable({ data, isLoading, lastRun }) {
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("rating");
  const [selectedCuisine, setSelectedCuisine] = useState("All");
  const [minimumRating, setMinimumRating] = useState("0");

  const cuisines = useMemo(() => {
    const unique = new Set(data.map((item) => item.cuisine).filter(Boolean));
    return ["All", ...unique];
  }, [data]);

  const filteredData = useMemo(() => {
    const query = search.trim().toLowerCase();

    return [...data]
      .filter((item) => {
        const matchesQuery =
          !query ||
          item.restaurant_name?.toLowerCase().includes(query) ||
          item.cuisine?.toLowerCase().includes(query);
        const matchesCuisine = selectedCuisine === "All" || item.cuisine === selectedCuisine;
        const matchesRating = (Number(item.rating) || 0) >= Number(minimumRating);
        return matchesQuery && matchesCuisine && matchesRating;
      })
      .sort((left, right) => {
        if (sortBy === "sentiment") {
          return getSentiment(right) - getSentiment(left);
        }

        if (sortBy === "name") {
          return (left.restaurant_name || "").localeCompare(right.restaurant_name || "");
        }

        return (Number(right.rating) || 0) - (Number(left.rating) || 0);
      });
  }, [data, minimumRating, search, selectedCuisine, sortBy]);

  if (!data.length && !isLoading) {
    return (
      <section className="results-panel empty-results">
        <span className="eyebrow">Results</span>
        <h2>No recommendations yet</h2>
        <p>Generate a manual query or upload a CSV file to start exploring recommendation results.</p>
      </section>
    );
  }

  const exportJson = () => {
    downloadFile(JSON.stringify(filteredData, null, 2), "recommendations.json", "application/json");
  };

  const exportCsv = () => {
    const rows = [
      ["restaurant_name", "cuisine", "rating", "sentiment_score"],
      ...filteredData.map((item) => [
        item.restaurant_name ?? "",
        item.cuisine ?? "",
        item.rating ?? "",
        item.sentiment_score ?? item.sentiment ?? "",
      ]),
    ];

    const content = rows
      .map((row) =>
        row
          .map((value) => `"${String(value).replaceAll('"', '""')}"`)
          .join(","),
      )
      .join("\n");

    downloadFile(content, "recommendations.csv", "text/csv;charset=utf-8;");
  };

  return (
    <section className="results-panel">
      <div className="section-heading results-heading">
        <div>
          <span className="eyebrow">Results</span>
          <h2>Recommendation intelligence board</h2>
        </div>
        <p>{lastRun ? `Last refreshed at ${lastRun.toLocaleTimeString()}` : "Awaiting first analysis run."}</p>
      </div>

      <div className="toolbar">
        <label className="toolbar-field search-field">
          <span>Search</span>
          <input
            value={search}
            placeholder="Find by restaurant or cuisine"
            onChange={(event) => setSearch(event.target.value)}
          />
        </label>

        <label className="toolbar-field">
          <span>Cuisine</span>
          <select value={selectedCuisine} onChange={(event) => setSelectedCuisine(event.target.value)}>
            {cuisines.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label className="toolbar-field">
          <span>Min rating</span>
          <select value={minimumRating} onChange={(event) => setMinimumRating(event.target.value)}>
            <option value="0">Any</option>
            <option value="3">3.0+</option>
            <option value="4">4.0+</option>
            <option value="4.5">4.5+</option>
          </select>
        </label>

        <label className="toolbar-field">
          <span>Sort by</span>
          <select value={sortBy} onChange={(event) => setSortBy(event.target.value)}>
            <option value="rating">Rating</option>
            <option value="sentiment">Sentiment</option>
            <option value="name">Name</option>
          </select>
        </label>

        <div className="toolbar-actions">
          <button type="button" className="ghost-button" onClick={exportJson}>
            Export JSON
          </button>
          <button type="button" className="primary-button" onClick={exportCsv}>
            Export CSV
          </button>
        </div>
      </div>

      <div className="summary-strip">
        <article>
          <span>Visible results</span>
          <strong>{filteredData.length}</strong>
        </article>
        <article>
          <span>Highest rating</span>
          <strong>{filteredData[0] ? Number(filteredData[0].rating || 0).toFixed(1) : "0.0"}</strong>
        </article>
        <article>
          <span>Strongest sentiment</span>
          <strong>
            {filteredData.length
              ? Math.max(...filteredData.map((item) => getSentiment(item))).toFixed(2)
              : "0.00"}
          </strong>
        </article>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Restaurant</th>
              <th>Cuisine</th>
              <th>Rating</th>
              <th>Sentiment</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {filteredData.length ? (
              filteredData.map((item, index) => {
                const rating = Number(item.rating) || 0;
                const sentiment = getSentiment(item);
                const badge =
                  rating >= 4.5 && sentiment >= 0.8
                    ? "Excellent fit"
                    : rating >= 4
                      ? "Promising"
                      : "Watchlist";

                return (
                  <tr key={`${item.restaurant_name || "restaurant"}-${index}`}>
                    <td>
                      <div className="restaurant-cell">
                        <strong>{item.restaurant_name || "Unknown restaurant"}</strong>
                        <span>Rank #{index + 1}</span>
                      </div>
                    </td>
                    <td>{item.cuisine || "Unknown"}</td>
                    <td>{rating.toFixed(1)}</td>
                    <td>{sentiment.toFixed(2)}</td>
                    <td>
                      <span className={`status-pill ${badge.toLowerCase().replaceAll(" ", "-")}`}>{badge}</span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="5" className="empty-table">
                  No rows match the current filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default RecommendationTable;
