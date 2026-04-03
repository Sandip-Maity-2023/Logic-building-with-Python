from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import math
import secrets
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field


DATA_FILE = Path(__file__).with_name("runtime_data.json")

RESTAURANT_NAME_MAP = {
    1: "Pizza Hut",
    2: "Dominos",
    3: "Beijing Street",
    4: "Kake Di Hatti",
    5: "Italian Joint",
    6: "Chinese Yum",
    7: "Sagar Ratna",
    8: "QDs",
    9: "D Cafe",
    10: "Tamasha",
    11: "Masala Trail",
}

DISH_META = {
    "chholebature": {"label": "Cholle Bhature", "cuisine": "North Indian"},
    "rajmachawal": {"label": "Rajma Chawal", "cuisine": "North Indian"},
    "dosa": {"label": "Dosa", "cuisine": "South Indian"},
    "idli": {"label": "Idli", "cuisine": "South Indian"},
    "noodles": {"label": "Noodles", "cuisine": "Chinese"},
    "chillypaneer": {"label": "Chilly Paneer", "cuisine": "Chinese"},
    "alootikki": {"label": "Aaloo Tikki", "cuisine": "Fast Food"},
    "vadapao": {"label": "Vada Pao", "cuisine": "Fast Food"},
    "garlicbread": {"label": "Garlic Bread", "cuisine": "Italian"},
    "pasta": {"label": "Pasta", "cuisine": "Italian"},
    "springroll": {"label": "Spring Roll", "cuisine": "Continental"},
    "ham": {"label": "Ham", "cuisine": "Continental"},
    "icecream": {"label": "Ice Cream", "cuisine": "Desserts"},
    "pastries": {"label": "Pastries", "cuisine": "Desserts"},
    "chocolates": {"label": "Chocolates", "cuisine": "Desserts"},
    "tea": {"label": "Tea", "cuisine": "Beverages"},
    "softdrinks": {"label": "Soft Drinks", "cuisine": "Beverages"},
    "juices": {"label": "Juices", "cuisine": "Beverages"},
}

MOOD_DEFAULTS = {
    "happie": ["Cholle Bhature", "Garlic Bread", "Dosa"],
    "angrie": ["Soft Drinks", "Pasta", "Spring Roll"],
    "dehydratie": ["Juices", "Soft Drinks", "Tea"],
    "depressie": ["Ice Cream", "Chocolates", "Pastries"],
    "excitie": ["Noodles", "Chilly Paneer", "Vada Pao"],
    "unwellie": ["Idli", "Tea", "Rajma Chawal"],
}

TRAINING_ROWS = [
    {"rating": 5.0, "distance": 7.0, "cost": 200.0, "yesno": 1},
    {"rating": 2.0, "distance": 10.0, "cost": 600.0, "yesno": 0},
    {"rating": 5.0, "distance": 1.0, "cost": 700.0, "yesno": 1},
    {"rating": 2.0, "distance": 1.0, "cost": 200.0, "yesno": 1},
    {"rating": 4.0, "distance": 12.0, "cost": 200.0, "yesno": 0},
    {"rating": 3.0, "distance": 20.0, "cost": 50.0, "yesno": 0},
    {"rating": 5.0, "distance": 15.0, "cost": 300.0, "yesno": 1},
    {"rating": 2.0, "distance": 4.0, "cost": 350.0, "yesno": 1},
    {"rating": 4.3, "distance": 4.0, "cost": 1200.0, "yesno": 0},
    {"rating": 3.7, "distance": 8.0, "cost": 200.0, "yesno": 1},
    {"rating": 2.0, "distance": 3.0, "cost": 400.0, "yesno": 1},
    {"rating": 4.6, "distance": 10.0, "cost": 250.0, "yesno": 1},
    {"rating": 1.3, "distance": 14.0, "cost": 1000.0, "yesno": 0},
    {"rating": 5.0, "distance": 4.0, "cost": 500.0, "yesno": 1},
    {"rating": 3.0, "distance": 5.0, "cost": 600.0, "yesno": 1},
    {"rating": 4.0, "distance": 2.0, "cost": 1200.0, "yesno": 0},
    {"rating": 3.5, "distance": 1.0, "cost": 350.0, "yesno": 1},
    {"rating": 1.0, "distance": 2.0, "cost": 300.0, "yesno": 1},
    {"rating": 4.0, "distance": 7.0, "cost": 1300.0, "yesno": 0},
    {"rating": 2.0, "distance": 5.0, "cost": 340.0, "yesno": 1},
]

SEED_RESTAURANTS = [
    {
        "id": 1,
        "name": "Pizza Hut",
        "latitude": 28.63,
        "longitude": 77.21,
        "rating": 3.5,
        "cost_for_two": 900,
        "rating_count": 5,
        "dishes": ["garlicbread", "pasta", "icecream", "tea", "juices"],
    },
    {
        "id": 2,
        "name": "Dominos",
        "latitude": 27.0,
        "longitude": 78.0,
        "rating": 4.0,
        "cost_for_two": 500,
        "rating_count": 10,
        "dishes": ["garlicbread", "pasta", "icecream", "chocolates", "tea", "juices"],
    },
    {
        "id": 3,
        "name": "Beijing Street",
        "latitude": 28.5,
        "longitude": 77.5,
        "rating": 3.0,
        "cost_for_two": 400,
        "rating_count": 7,
        "dishes": ["noodles", "chillypaneer", "alootikki", "vadapao", "springroll", "ham"],
    },
    {
        "id": 4,
        "name": "Kake Di Hatti",
        "latitude": 29.0,
        "longitude": 76.9,
        "rating": 5.0,
        "cost_for_two": 200,
        "rating_count": 10,
        "dishes": [
            "chholebature",
            "rajmachawal",
            "dosa",
            "idli",
            "noodles",
            "chillypaneer",
            "icecream",
            "softdrinks",
        ],
    },
    {
        "id": 5,
        "name": "Italian Joint",
        "latitude": 25.0,
        "longitude": 79.0,
        "rating": 4.0,
        "cost_for_two": 300,
        "rating_count": 9,
        "dishes": [
            "noodles",
            "chillypaneer",
            "garlicbread",
            "pasta",
            "springroll",
            "ham",
            "tea",
            "juices",
        ],
    },
    {
        "id": 6,
        "name": "Chinese Yum",
        "latitude": 28.0,
        "longitude": 78.0,
        "rating": 3.0,
        "cost_for_two": 400,
        "rating_count": 5,
        "dishes": [
            "dosa",
            "idli",
            "noodles",
            "chillypaneer",
            "icecream",
            "tea",
            "softdrinks",
            "juices",
        ],
    },
    {
        "id": 7,
        "name": "Sagar Ratna",
        "latitude": 30.0,
        "longitude": 79.0,
        "rating": 4.9,
        "cost_for_two": 450,
        "rating_count": 7,
        "dishes": [
            "chholebature",
            "rajmachawal",
            "dosa",
            "idli",
            "noodles",
            "chillypaneer",
            "tea",
            "softdrinks",
        ],
    },
    {
        "id": 8,
        "name": "QDs",
        "latitude": 29.9,
        "longitude": 76.9,
        "rating": 2.9,
        "cost_for_two": 1000,
        "rating_count": 4,
        "dishes": [
            "noodles",
            "chillypaneer",
            "garlicbread",
            "pasta",
            "springroll",
            "ham",
            "chocolates",
            "tea",
            "juices",
        ],
    },
    {
        "id": 9,
        "name": "D Cafe",
        "latitude": 29.0,
        "longitude": 78.0,
        "rating": 4.0,
        "cost_for_two": 500,
        "rating_count": 10,
        "dishes": list(DISH_META.keys()),
    },
    {
        "id": 10,
        "name": "Tamasha",
        "latitude": 27.9,
        "longitude": 78.5,
        "rating": 2.9,
        "cost_for_two": 300,
        "rating_count": 10,
        "dishes": [
            "chholebature",
            "rajmachawal",
            "dosa",
            "idli",
            "garlicbread",
            "pasta",
            "springroll",
            "ham",
            "tea",
            "softdrinks",
        ],
    },
    {
        "id": 11,
        "name": "Masala Trail",
        "latitude": 30.0,
        "longitude": 77.0,
        "rating": 5.0,
        "cost_for_two": 500,
        "rating_count": 8,
        "dishes": [
            "chholebature",
            "rajmachawal",
            "dosa",
            "idli",
            "noodles",
            "chillypaneer",
            "alootikki",
            "vadapao",
            "softdrinks",
        ],
    },
]


def build_seed_state() -> dict:
    mood_votes = []
    for key, dishes in MOOD_DEFAULTS.items():
        for index, dish in enumerate(dishes):
            mood_votes.append({"dish": dish, "mood": key, "weight": 3 - index})

    restaurants = []
    for restaurant in SEED_RESTAURANTS:
        cuisines = sorted({DISH_META[dish]["cuisine"] for dish in restaurant["dishes"]})
        restaurants.append({**restaurant, "cuisines": cuisines})

    return {
        "restaurants": restaurants,
        "training_rows": copy.deepcopy(TRAINING_ROWS),
        "mood_votes": mood_votes,
        "sellers": [
            {
                "id": 1,
                "name": "F",
                "address": "F",
                "items": "F",
            }
        ],
        "users": [],
        "sessions": {},
        "feedback": [],
    }


def load_state() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    state = build_seed_state()
    save_state(state)
    return state


def save_state(state: dict) -> None:
    DATA_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def distance_between(latitude: float, longitude: float, restaurant: dict) -> float:
    return math.sqrt(
        ((restaurant["latitude"] - latitude) ** 2) + ((restaurant["longitude"] - longitude) ** 2)
    ) * 111


def restaurant_score(restaurant: dict, distance_km: float, sentiment_bias: float = 0.0) -> float:
    rating_score = clamp(restaurant["rating"] / 5, 0, 1)
    cost_score = clamp(1 - (restaurant["cost_for_two"] / 1400), 0, 1)
    distance_score = clamp(1 - (distance_km / 2500), 0, 1)
    return round((rating_score * 0.45) + (cost_score * 0.25) + (distance_score * 0.2) + sentiment_bias, 4)


def serialize_recommendation(restaurant: dict, distance_km: float, score: float, cuisine_hint: str | None = None) -> dict:
    primary_cuisine = cuisine_hint or (restaurant["cuisines"][0] if restaurant["cuisines"] else "Mixed")
    return {
        "restaurant_name": restaurant["name"],
        "cuisine": primary_cuisine,
        "rating": round(restaurant["rating"], 2),
        "sentiment_score": round(clamp(score, 0, 1), 2),
        "distance_km": round(distance_km, 1),
        "cost_for_two": restaurant["cost_for_two"],
        "recommended_dishes": [DISH_META[dish]["label"] for dish in restaurant["dishes"][:4]],
    }


def get_restaurant_by_name(state: dict, name: str) -> dict:
    for restaurant in state["restaurants"]:
        if restaurant["name"].lower() == name.lower():
            return restaurant
    raise HTTPException(status_code=404, detail="Restaurant not found.")


class ManualRecommendationInput(BaseModel):
    cuisine: str = Field(default="")
    rating: float = Field(default=4.0, ge=0, le=5)
    sentiment: float = Field(default=0.75, ge=0, le=1)


class AuthInput(BaseModel):
    username: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class DishQuery(BaseModel):
    dish: str
    latitude: float = 28.61
    longitude: float = 77.2


class MoodFeedbackInput(BaseModel):
    token: str | None = None
    restaurant: str
    food: str
    mood: str
    rating: float = Field(ge=0, le=5)


class SellerInput(BaseModel):
    name: str = Field(min_length=2)
    address: str = Field(min_length=4)
    items: str = Field(min_length=2)


for model in (
    ManualRecommendationInput,
    AuthInput,
    LoginInput,
    DishQuery,
    MoodFeedbackInput,
    SellerInput,
):
    model.model_rebuild()


app = FastAPI(title="MindAI MoodieFoodie API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE = load_state()


@app.get("/")
def root() -> dict:
    return {"message": "MindAI backend is running."}


@app.get("/catalog")
def catalog() -> dict:
    dishes = [
        {"slug": slug, "label": meta["label"], "cuisine": meta["cuisine"]}
        for slug, meta in DISH_META.items()
    ]
    return {
        "dishes": dishes,
        "moods": [{"slug": key, "label": key.replace("ie", "ie ").title().replace("  ", " ").strip()} for key in MOOD_DEFAULTS],
        "restaurants": [
            {
                "name": restaurant["name"],
                "rating": restaurant["rating"],
                "cost_for_two": restaurant["cost_for_two"],
                "cuisines": restaurant["cuisines"],
            }
            for restaurant in STATE["restaurants"]
        ],
        "sellers": STATE["sellers"],
    }


@app.post("/recommend")
def recommend(payload: ManualRecommendationInput) -> dict:
    cuisine = payload.cuisine.strip().lower()
    matches = []

    for restaurant in STATE["restaurants"]:
        restaurant_cuisines = [item.lower() for item in restaurant["cuisines"]]
        if cuisine and cuisine not in restaurant_cuisines and cuisine not in restaurant["name"].lower():
            continue

        distance_km = distance_between(28.61, 77.2, restaurant)
        base_score = restaurant_score(restaurant, distance_km, payload.sentiment * 0.1)
        rating_penalty = max(0.0, payload.rating - restaurant["rating"]) * 0.12
        final_score = clamp(base_score - rating_penalty, 0, 1)
        matches.append(serialize_recommendation(restaurant, distance_km, final_score, payload.cuisine or None))

    matches.sort(key=lambda item: (item["sentiment_score"], item["rating"]), reverse=True)
    return {"recommendations": matches[:10]}


@app.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    recommendations = []

    for row in reader:
        rating = float(row.get("rating") or 0)
        sentiment = float(row.get("sentiment_score") or row.get("sentiment") or 0)
        restaurant_name = row.get("restaurant_name") or row.get("name") or "Unknown restaurant"
        cuisine = row.get("cuisine") or "Mixed"
        score = clamp((rating / 5) * 0.6 + sentiment * 0.4, 0, 1)
        recommendations.append(
            {
                "restaurant_name": restaurant_name,
                "cuisine": cuisine,
                "rating": round(rating, 2),
                "sentiment_score": round(score, 2),
            }
        )

    recommendations.sort(key=lambda item: (item["sentiment_score"], item["rating"]), reverse=True)
    return {"recommendations": recommendations}


@app.post("/dish-recommendations")
def dish_recommendations(payload: DishQuery) -> dict:
    dish = payload.dish.strip().lower()
    if dish not in DISH_META:
        raise HTTPException(status_code=404, detail="Dish not found.")

    results = []
    for restaurant in STATE["restaurants"]:
        if dish not in restaurant["dishes"]:
            continue
        distance_km = distance_between(payload.latitude, payload.longitude, restaurant)
        score = restaurant_score(restaurant, distance_km, 0.05)
        entry = serialize_recommendation(restaurant, distance_km, score, DISH_META[dish]["cuisine"])
        entry["dish"] = DISH_META[dish]["label"]
        results.append(entry)

    results.sort(key=lambda item: (item["sentiment_score"], -item["distance_km"]), reverse=True)
    return {"recommendations": results}


@app.get("/mood-recommendations/{mood}")
def mood_recommendations(mood: str) -> dict:
    mood_key = mood.strip().lower()
    if mood_key not in MOOD_DEFAULTS:
        raise HTTPException(status_code=404, detail="Mood not found.")

    scores = {}
    for vote in STATE["mood_votes"]:
        if vote["mood"] != mood_key:
            continue
        scores[vote["dish"]] = scores.get(vote["dish"], 0) + vote.get("weight", 1)

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    dishes = [name for name, _ in ranked] or MOOD_DEFAULTS[mood_key]

    return {
        "mood": mood_key,
        "recommendations": [
            {"dish": dish, "score": scores.get(dish, len(dishes) - index), "cuisine": next((meta["cuisine"] for meta in DISH_META.values() if meta["label"] == dish), "Mixed")}
            for index, dish in enumerate(dishes)
        ],
    }


@app.post("/feedback")
def submit_feedback(payload: MoodFeedbackInput) -> dict:
    restaurant = get_restaurant_by_name(STATE, payload.restaurant)
    new_count = restaurant["rating_count"] + 1
    restaurant["rating"] = round(((restaurant["rating"] * restaurant["rating_count"]) + payload.rating) / new_count, 2)
    restaurant["rating_count"] = new_count

    STATE["feedback"].append(payload.model_dump())
    STATE["mood_votes"].append({"dish": payload.food, "mood": payload.mood.lower(), "weight": 1})
    save_state(STATE)

    return {
        "message": "Feedback saved successfully.",
        "restaurant": {
            "name": restaurant["name"],
            "rating": restaurant["rating"],
            "rating_count": restaurant["rating_count"],
        },
    }


@app.post("/sellers")
def register_seller(payload: SellerInput) -> dict:
    seller = {
        "id": len(STATE["sellers"]) + 1,
        "name": payload.name,
        "address": payload.address,
        "items": payload.items,
    }
    STATE["sellers"].append(seller)
    save_state(STATE)
    return {"message": "Seller request submitted.", "seller": seller}


@app.post("/auth/signup")
def signup(payload: AuthInput) -> dict:
    for user in STATE["users"]:
        if user["email"].lower() == payload.email.lower():
            raise HTTPException(status_code=400, detail="This email is already registered.")

    user = {
        "id": len(STATE["users"]) + 1,
        "username": payload.username,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
    }
    STATE["users"].append(user)
    token = secrets.token_hex(16)
    STATE["sessions"][token] = user["email"]
    save_state(STATE)
    return {"message": "Account created.", "token": token, "user": {"username": user["username"], "email": user["email"]}}


@app.post("/auth/login")
def login(payload: LoginInput) -> dict:
    password_hash = hash_password(payload.password)
    for user in STATE["users"]:
        if user["email"].lower() == payload.email.lower() and user["password_hash"] == password_hash:
            token = secrets.token_hex(16)
            STATE["sessions"][token] = user["email"]
            save_state(STATE)
            return {"message": "Logged in.", "token": token, "user": {"username": user["username"], "email": user["email"]}}

    raise HTTPException(status_code=401, detail="Invalid email or password.")


@app.get("/auth/me")
def me(token: str) -> dict:
    email = STATE["sessions"].get(token)
    if not email:
        raise HTTPException(status_code=401, detail="Session not found.")

    for user in STATE["users"]:
        if user["email"] == email:
            return {"user": {"username": user["username"], "email": user["email"]}}

    raise HTTPException(status_code=401, detail="Session not found.")
