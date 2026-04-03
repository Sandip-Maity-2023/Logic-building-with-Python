import React, { useEffect, useMemo, useState } from "react";
import RecommendationTable from "./RecommendationTable";
import "./App.css";
import AuthPanel from "./components/AuthPanel";
import DishExplorer from "./components/DishExplorer";
import FeedbackStudio from "./components/FeedbackStudio";
import ManualInput from "./components/ManualInput";
import MoodBoard from "./components/MoodBoard";
import SellerForm from "./components/SellerForm";
import UploadCsv from "./components/UploadCsv";
import {
  fetchCatalog,
  getDishRecommendations,
  getMoodRecommendations,
  getRecommendations,
  login,
  registerSeller,
  signup,
  submitFeedback,
  uploadCSV,
} from "./api";
import panImage from "./assets/pan.webp";
import riceImage from "./assets/rice.jpg";
import wallImage from "./assets/w.jpg";

const STORAGE_KEY = "mindai-dashboard-history";
const SESSION_KEY = "mindai-session";
const images = [panImage, wallImage, riceImage];

const normaliseList = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.recommendations)) return payload.recommendations;
  if (Array.isArray(payload?.data)) return payload.data;
  return [];
};

const moodLabel = (value) =>
  ({
    happie: "Happie",
    angrie: "Angrie",
    dehydratie: "Dehydratie",
    depressie: "Depressie",
    excitie: "Excitie",
    unwellie: "Unwellie",
  })[value] || value;

function App() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [catalog, setCatalog] = useState({
    dishes: [],
    moods: [],
    restaurants: [],
    sellers: [],
  });
  const [bgIndex, setBgIndex] = useState(0);
  const [activeMood, setActiveMood] = useState("");
  const [moodRecommendations, setMoodRecommendations] = useState([]);
  const [history, setHistory] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });
  const [session, setSession] = useState(() => {
    try {
      const stored = localStorage.getItem(SESSION_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });
  const [lastRun, setLastRun] = useState(null);
  const [activeSource, setActiveSource] = useState("manual");

  useEffect(() => {
    const interval = window.setInterval(() => {
      setBgIndex((prev) => (prev + 1) % images.length);
    }, 10000);

    return () => window.clearInterval(interval);
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history.slice(0, 6)));
  }, [history]);

  useEffect(() => {
    if (session) {
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
      return;
    }

    localStorage.removeItem(SESSION_KEY);
  }, [session]);

  useEffect(() => {
    const loadCatalog = async () => {
      try {
        const response = await fetchCatalog();
        setCatalog({
          ...response.data,
          moods: (response.data.moods || []).map((item) => ({
            ...item,
            label: moodLabel(item.slug),
          })),
        });
      } catch {
        setError("The feature catalog could not be loaded. Start the backend and refresh.");
      }
    };

    loadCatalog();
  }, []);

  const metrics = useMemo(() => {
    if (!results.length) {
      return {
        averageRating: "0.0",
        averageSentiment: "0.00",
        cuisines: 0,
        topRestaurant: "No data yet",
      };
    }

    const totals = results.reduce(
      (accumulator, item) => {
        const rating = Number(item.rating) || 0;
        const sentiment = Number(item.sentiment_score ?? item.sentiment) || 0;
        accumulator.rating += rating;
        accumulator.sentiment += sentiment;
        accumulator.cuisines.add(item.cuisine || "Unknown");
        return accumulator;
      },
      { rating: 0, sentiment: 0, cuisines: new Set() },
    );

    const bestMatch = [...results].sort(
      (left, right) =>
        (Number(right.rating) || 0) - (Number(left.rating) || 0) ||
        (Number(right.sentiment_score ?? right.sentiment) || 0) -
          (Number(left.sentiment_score ?? left.sentiment) || 0),
    )[0];

    return {
      averageRating: (totals.rating / results.length).toFixed(1),
      averageSentiment: (totals.sentiment / results.length).toFixed(2),
      cuisines: totals.cuisines.size,
      topRestaurant: bestMatch?.restaurant_name || "No data yet",
    };
  }, [results]);

  const saveRun = (entry) => {
    setHistory((current) =>
      [entry, ...current.filter((item) => item.id !== entry.id)].slice(0, 6),
    );
  };

  const refreshCatalog = async () => {
    const response = await fetchCatalog();
    setCatalog({
      ...response.data,
      moods: (response.data.moods || []).map((item) => ({
        ...item,
        label: moodLabel(item.slug),
      })),
    });
  };

  const handleManualSubmit = async (formValues) => {
    setIsLoading(true);
    setError("");
    setActiveSource("manual");

    try {
      const response = await getRecommendations(formValues);
      const nextResults = normaliseList(response.data);
      setResults(nextResults);
      setLastRun(new Date());

      saveRun({
        id: `manual-${Date.now()}`,
        type: "Manual",
        label: `${formValues.cuisine || "Any cuisine"} | rating ${formValues.rating} | sentiment ${formValues.sentiment}`,
        count: nextResults.length,
      });
    } catch (requestError) {
      setError(
        requestError?.response?.data?.detail ||
          requestError?.message ||
          "Unable to fetch recommendations right now.",
      );
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUploadSubmit = async (file) => {
    setIsLoading(true);
    setError("");
    setActiveSource("upload");

    try {
      const response = await uploadCSV(file);
      const nextResults = normaliseList(response.data);
      setResults(nextResults);
      setLastRun(new Date());

      saveRun({
        id: `upload-${Date.now()}`,
        type: "CSV",
        label: file.name,
        count: nextResults.length,
      });
    } catch (requestError) {
      setError(
        requestError?.response?.data?.detail ||
          requestError?.message ||
          "The CSV upload could not be processed.",
      );
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDishSubmit = async (payload) => {
    setIsLoading(true);
    setError("");
    setActiveSource("dish");

    try {
      const response = await getDishRecommendations(payload);
      const nextResults = normaliseList(response.data);
      setResults(nextResults);
      setLastRun(new Date());
      const selectedDish =
        catalog.dishes.find((item) => item.slug === payload.dish)?.label ||
        payload.dish;

      saveRun({
        id: `dish-${Date.now()}`,
        type: "Dish",
        label: selectedDish,
        count: nextResults.length,
      });
    } catch (requestError) {
      setError(
        requestError?.response?.data?.detail ||
          "Dish recommendations are unavailable right now.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleMoodPick = async (mood) => {
    setActiveMood(mood);
    setError("");

    try {
      const response = await getMoodRecommendations(mood);
      setMoodRecommendations(response.data.recommendations || []);
    } catch (requestError) {
      setError(
        requestError?.response?.data?.detail ||
          "Mood suggestions could not be loaded.",
      );
    }
  };

  const handleAuth = async (mode, form) => {
    const payload =
      mode === "login"
        ? { email: form.email, password: form.password }
        : {
            username: form.username,
            email: form.email,
            password: form.password,
          };

    const response = mode === "login" ? await login(payload) : await signup(payload);
    setSession(response.data);
    return response.data;
  };

  const handleFeedbackSubmit = async (payload) => {
    setIsLoading(true);
    setError("");

    try {
      const response = await submitFeedback(payload);
      await refreshCatalog();
      return response.data;
    } catch (requestError) {
      setError(
        requestError?.response?.data?.detail ||
          "Feedback could not be saved.",
      );
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const handleSellerSubmit = async (payload) => {
    setIsLoading(true);
    setError("");

    try {
      const response = await registerSeller(payload);
      await refreshCatalog();
      return response.data;
    } catch (requestError) {
      setError(
        requestError?.response?.data?.detail ||
          "Seller registration failed.",
      );
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <span className="eyebrow">MindAI</span>
          <h1>
            Mood-based food discovery and restaurant intelligence in one place.
          </h1>
          <p className="hero-text">
            MindAI now folds in the full MoodieFoodie idea set: manual analysis,
            CSV ranking, dish-level exploration, mood-based food picks, seller
            onboarding, and community feedback loops.
          </p>

          <div className="hero-actions">
            <a href="#workspace" className="primary-action">
              Launch workspace
            </a>
            <button
              type="button"
              className="secondary-action"
              onClick={() => {
                setResults([]);
                setError("");
              }}
            >
              Clear results
            </button>
          </div>

          <div className="hero-stats">
            <article>
              <strong>{results.length || 0}</strong>
              <span>Recommendations visible</span>
            </article>
            <article>
              <strong>{metrics.averageRating}</strong>
              <span>Average rating</span>
            </article>
            <article>
              <strong>{metrics.averageSentiment}</strong>
              <span>Average sentiment</span>
            </article>
            <article>
              <strong>{catalog.sellers.length}</strong>
              <span>Sellers onboarded</span>
            </article>
          </div>
        </div>

        <div className="hero-visual">
          <div
            className="signal-card signal-primary"
            style={{ backgroundImage: `url(${images[bgIndex]})` }}
          >
            <span>Top signal</span>
            <strong>{metrics.topRestaurant}</strong>
            <p>Highest-performing recommendation in the current result set.</p>
          </div>

          <div className="signal-grid">
            <div className="signal-card">
              <span>Active mode</span>
              <strong>
                {activeSource === "manual"
                  ? "Manual analysis"
                  : activeSource === "upload"
                    ? "CSV intelligence"
                    : "Dish ranking"}
              </strong>
            </div>
            <div className="signal-card">
              <span>Diverse cuisines</span>
              <strong>{metrics.cuisines}</strong>
            </div>
            <div className="signal-card">
              <span>Last run</span>
              <strong>
                {lastRun ? lastRun.toLocaleTimeString() : "Not yet"}
              </strong>
            </div>
            <div className="signal-card accent-card">
              <span>Mind state</span>
              <strong>{activeMood ? moodLabel(activeMood) : "Ready to map moods"}</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="workspace" id="workspace">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Interactive Workspace</span>
            <h2>Choose how you want to generate recommendations</h2>
          </div>
          <p>
            Use guided inputs for quick experiments or upload a dataset to
            analyze many records at once.
          </p>
        </div>

        <div className="workspace-grid">
          <ManualInput onSubmit={handleManualSubmit} isLoading={isLoading} />
          <UploadCsv onUpload={handleUploadSubmit} isLoading={isLoading} />
        </div>

        {error ? (
          <div className="feedback-banner error-banner">{error}</div>
        ) : null}
      </section>

      <section className="workspace">
        <div className="section-heading">
          <div>
            <span className="eyebrow">MoodieFoodie Features</span>
            <h2>Explore cravings, moods, community, and sellers</h2>
          </div>
          <p>
            This section ports the old project's category browsing, mood-based
            discovery, seller onboarding, and feedback training into MindAI.
          </p>
        </div>

        <div className="workspace-grid">
          <DishExplorer
            dishes={catalog.dishes}
            onSubmit={handleDishSubmit}
            isLoading={isLoading}
          />
          <MoodBoard
            moods={catalog.moods}
            activeMood={activeMood}
            recommendations={moodRecommendations}
            onPick={handleMoodPick}
            isLoading={false}
          />
        </div>
      </section>

      <section className="workspace">
        <div className="workspace-grid triple-grid">
          <AuthPanel
            session={session}
            onLogin={handleAuth}
            isLoading={isLoading}
          />
          <FeedbackStudio
            restaurants={catalog.restaurants}
            dishes={catalog.dishes}
            moods={catalog.moods}
            token={session?.token}
            onSubmit={handleFeedbackSubmit}
            isLoading={isLoading}
          />
          <SellerForm
            sellers={catalog.sellers}
            onSubmit={handleSellerSubmit}
            isLoading={isLoading}
          />
        </div>
      </section>

      <section className="history-panel">
        <div className="section-heading compact">
          <div>
            <span className="eyebrow">Recent Activity</span>
            <h2>Pick up where you left off</h2>
          </div>
        </div>

        <div className="history-list">
          {history.length ? (
            history.map((item) => (
              <article className="history-card" key={item.id}>
                <span>{item.type}</span>
                <strong>{item.label}</strong>
                <p>
                  {item.count} recommendation{item.count === 1 ? "" : "s"}{" "}
                  returned
                </p>
              </article>
            ))
          ) : (
            <article className="history-card empty-history">
              <span>No runs yet</span>
              <strong>
                Your recent searches, dish explorations, and CSV uploads will
                appear here.
              </strong>
            </article>
          )}
        </div>
      </section>

      <RecommendationTable
        data={results}
        isLoading={isLoading}
        lastRun={lastRun}
      />
    </div>
  );
}

export default App;
