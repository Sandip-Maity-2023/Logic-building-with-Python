import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.PROD ? "/api" : "http://localhost:8000");

const API = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getRecommendations = (data) => API.post("/recommend", data);

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/upload", formData);
};

export const fetchCatalog = () => API.get("/catalog");

export const getDishRecommendations = (data) =>
  API.post("/dish-recommendations", data);

export const getMoodRecommendations = (mood) =>
  API.get(`/mood-recommendations/${mood}`);

export const submitFeedback = (data) => API.post("/feedback", data);

export const registerSeller = (data) => API.post("/sellers", data);

export const signup = (data) => API.post("/auth/signup", data);

export const login = (data) => API.post("/auth/login", data);
