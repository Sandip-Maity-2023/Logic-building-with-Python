import json
import os
from pathlib import Path

import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from models.recommendation import recommend_restaurants
from utils.preprocessing import load_restaurant_data, preprocess_data


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ALLOWED_EXTENSIONS = {"csv"}
DEFAULT_DATASET = "Zomato-data-.csv"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "restaurant_analytics_secret")
app.config["UPLOAD_FOLDER"] = DATA_DIR


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def dataset_path(filename):
    safe_name = secure_filename(filename)
    return DATA_DIR / safe_name


def available_datasets():
    DATA_DIR.mkdir(exist_ok=True)
    return sorted(path.name for path in DATA_DIR.glob("*.csv"))


def active_dataset(filename=None):
    files = available_datasets()
    if filename and filename in files:
        return filename
    if DEFAULT_DATASET in files:
        return DEFAULT_DATASET
    return files[0] if files else None


def sentiment_label(rating):
    if rating >= 4:
        return "Positive"
    if rating >= 3:
        return "Neutral"
    return "Negative"


def add_sentiment(df):
    df = df.copy()
    df["sentiment"] = df["rate"].apply(sentiment_label)
    return df


def score_prediction(rating, votes, cost, online_order, book_table):
    online_bonus = 0.18 if online_order == "Yes" else 0
    table_bonus = 0.15 if book_table == "Yes" else 0
    vote_signal = min(float(votes), 5000) / 5000
    value_signal = max(0, 1 - min(float(cost), 1200) / 1200)
    score = (float(rating) * 18) + (vote_signal * 10) + (value_signal * 6) + online_bonus + table_bonus
    return round(max(0, min(score, 100)), 1)


def build_charts(df):
    type_counts = df["listed_in(type)"].value_counts()
    sentiment_counts = df["sentiment"].value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0)
    rating_counts = df["rate"].round(1).value_counts().sort_index()
    top_votes = df.nlargest(10, "votes").sort_values("votes", ascending=False)
    cost_rating = df.groupby("listed_in(type)", as_index=False).agg(
        avg_rating=("rate", "mean"),
        avg_cost=("approx_cost(for two people)", "mean"),
        restaurants=("name", "count"),
    )

    return {
        "types": {
            "labels": type_counts.index.tolist(),
            "values": type_counts.astype(int).tolist(),
        },
        "ratings": {
            "labels": [str(label) for label in rating_counts.index.tolist()],
            "values": rating_counts.astype(int).tolist(),
        },
        "sentiment": {
            "labels": sentiment_counts.index.tolist(),
            "values": sentiment_counts.astype(int).tolist(),
        },
        "votes": {
            "labels": top_votes["name"].tolist(),
            "values": top_votes["votes"].astype(int).tolist(),
        },
        "cost_rating": {
            "points": [
                {
                    "x": float(round(row["avg_cost"], 2)),
                    "y": float(round(row["avg_rating"], 2)),
                    "r": int(max(6, min(24, int(row["restaurants"]) * 3))),
                    "label": row["listed_in(type)"],
                }
                for _, row in cost_rating.iterrows()
            ]
        },
    }


def dashboard_payload(filename):
    df = add_sentiment(load_restaurant_data(dataset_path(filename)))
    top = df.sort_values(["rate", "votes"], ascending=False).iloc[0]
    kpis = {
        "total_restaurants": len(df),
        "avg_rating": round(df["rate"].mean(), 2),
        "avg_cost": int(round(df["approx_cost(for two people)"].mean())),
        "online_percent": round((df["online_order"].eq("Yes").mean()) * 100, 1),
        "top_restaurant": top["name"],
        "top_rating": top["rate"],
    }
    table = df.sort_values(["rate", "votes"], ascending=False).head(12).to_dict(orient="records")
    return df, kpis, table, build_charts(df)


@app.route("/")
def home():
    filename = active_dataset(request.args.get("filename"))
    if not filename:
        return redirect(url_for("upload_file"))
    return redirect(url_for("dashboard", filename=filename))


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("Please choose a CSV file.")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only CSV files are supported.")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = dataset_path(filename)
        file.save(filepath)
        preprocess_data(filepath)
        flash("Dataset uploaded and cleaned successfully.")
        return redirect(url_for("dashboard", filename=filename))

    return render_template("upload.html", datasets=available_datasets())


@app.route("/dashboard/<filename>")
def dashboard(filename):
    filename = active_dataset(filename)
    if not filename:
        flash("Upload a dataset to start.")
        return redirect(url_for("upload_file"))

    df, kpis, top_table, charts = dashboard_payload(filename)
    return render_template(
        "dashboard.html",
        filename=filename,
        datasets=available_datasets(),
        kpis=kpis,
        top_table=top_table,
        charts=charts,
        columns=df.columns.tolist(),
    )


@app.route("/search/<filename>")
def search(filename):
    filename = active_dataset(filename)
    df = add_sentiment(load_restaurant_data(dataset_path(filename)))

    query = request.args.get("q", "").strip()
    restaurant_type = request.args.get("type", "All")
    online_order = request.args.get("online_order", "All")
    min_rating = float(request.args.get("min_rating", 0) or 0)
    max_cost = float(request.args.get("max_cost", df["approx_cost(for two people)"].max()) or 0)

    filtered = df.copy()
    if query:
        filtered = filtered[filtered["name"].str.contains(query, case=False, na=False)]
    if restaurant_type != "All":
        filtered = filtered[filtered["listed_in(type)"] == restaurant_type]
    if online_order != "All":
        filtered = filtered[filtered["online_order"] == online_order]
    filtered = filtered[(filtered["rate"] >= min_rating) & (filtered["approx_cost(for two people)"] <= max_cost)]
    filtered = filtered.sort_values(["rate", "votes"], ascending=False)

    return render_template(
        "search.html",
        filename=filename,
        results=filtered.head(50).to_dict(orient="records"),
        count=len(filtered),
        types=sorted(df["listed_in(type)"].dropna().unique()),
        filters={
            "q": query,
            "type": restaurant_type,
            "online_order": online_order,
            "min_rating": min_rating,
            "max_cost": int(max_cost),
        },
    )


@app.route("/recommend/<filename>", methods=["GET", "POST"])
def recommend(filename):
    filename = active_dataset(filename)
    df = add_sentiment(load_restaurant_data(dataset_path(filename)))

    preferences = {
        "restaurant_type": request.form.get("restaurant_type", "All"),
        "online_order": request.form.get("online_order", "All"),
        "book_table": request.form.get("book_table", "All"),
        "max_cost": int(request.form.get("max_cost", df["approx_cost(for two people)"].max()) or 0),
        "min_rating": float(request.form.get("min_rating", 3.5) or 0),
    }
    recommendations = recommend_restaurants(dataset_path(filename), preferences)

    return render_template(
        "recommendation.html",
        filename=filename,
        recommendations=recommendations,
        types=sorted(df["listed_in(type)"].dropna().unique()),
        preferences=preferences,
    )


@app.route("/sentiment/<filename>")
def sentiment(filename):
    filename = active_dataset(filename)
    df = add_sentiment(load_restaurant_data(dataset_path(filename)))
    sentiment_counts = df["sentiment"].value_counts().to_dict()
    sentiment_rows = df.sort_values(["rate", "votes"], ascending=False).head(25).to_dict(orient="records")
    charts = build_charts(df)
    return render_template(
        "analytics.html",
        filename=filename,
        sentiment_counts=sentiment_counts,
        sentiment_rows=sentiment_rows,
        sentiment_chart=charts["sentiment"],
        rating_chart=charts["ratings"],
    )


@app.route("/predict/<filename>", methods=["GET", "POST"])
def predict(filename):
    filename = active_dataset(filename)
    prediction = None
    form = {
        "rating": request.form.get("rating", "4.0"),
        "votes": request.form.get("votes", "250"),
        "cost": request.form.get("cost", "500"),
        "online_order": request.form.get("online_order", "Yes"),
        "book_table": request.form.get("book_table", "No"),
    }
    if request.method == "POST":
        prediction = score_prediction(
            form["rating"], form["votes"], form["cost"], form["online_order"], form["book_table"]
        )
    return render_template("prediction.html", filename=filename, prediction=prediction, form=form)


@app.context_processor
def inject_globals():
    return {"json": json, "active_dataset": active_dataset()}


if __name__ == "__main__":
    app.run(debug=True)
