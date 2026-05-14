from utils.preprocessing import load_restaurant_data


def _preference_score(row, preferences):
    score = (row["rate"] * 18) + min(row["votes"], 5000) / 80

    max_cost = preferences.get("max_cost")
    if max_cost:
        score += max(0, (max_cost - row["approx_cost(for two people)"]) / max_cost) * 8

    if row["online_order"] == "Yes":
        score += 2
    if row["book_table"] == "Yes":
        score += 2

    return round(score, 2)


def recommend_restaurants(filepath, preferences):
    df = load_restaurant_data(filepath)
    filtered = df.copy()

    restaurant_type = preferences.get("restaurant_type", "All")
    online_order = preferences.get("online_order", "All")
    book_table = preferences.get("book_table", "All")
    max_cost = int(preferences.get("max_cost") or filtered["approx_cost(for two people)"].max())
    min_rating = float(preferences.get("min_rating") or 0)

    if restaurant_type != "All":
        filtered = filtered[filtered["listed_in(type)"] == restaurant_type]
    if online_order != "All":
        filtered = filtered[filtered["online_order"] == online_order]
    if book_table != "All":
        filtered = filtered[filtered["book_table"] == book_table]

    filtered = filtered[
        (filtered["approx_cost(for two people)"] <= max_cost)
        & (filtered["rate"] >= min_rating)
    ].copy()

    if filtered.empty:
        filtered = df[df["rate"] >= min_rating].copy()

    filtered["recommendation_score"] = filtered.apply(
        lambda row: _preference_score(row, preferences), axis=1
    )
    filtered = filtered.sort_values(["recommendation_score", "rate", "votes"], ascending=False)

    return filtered.head(12).to_dict(orient="records")
