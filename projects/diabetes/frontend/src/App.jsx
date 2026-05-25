import React, { useState } from "react";
import axios from "axios";

function App() {

  const [formData, setFormData] = useState({

    Pregnancies: "",
    Glucose: "",
    BloodPressure: "",
    SkinThickness: "",
    Insulin: "",
    BMI: "",
    DiabetesPedigreeFunction: "",
    Age: ""

  });

  const [result, setResult] = useState("");

  const [confidence, setConfidence] = useState("");

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {

    setFormData({

      ...formData,
      [e.target.name]: e.target.value

    });
  };

  const handleSubmit = async (e) => {

    e.preventDefault();

    setLoading(true);

    try {

      const response = await axios.post(

        "https://logic-building-with-python.onrender.com/predict",

        formData

      );

      setResult(response.data.prediction);

      setConfidence(response.data.confidence);

    }

    catch (error) {

      console.log(error);

      alert("Error connecting to backend");

    }

    setLoading(false);
  };

  return (

    <div style={styles.container}>

      <div style={styles.overlay}></div>

      <div style={styles.card}>

        <div style={styles.header}>

          <div style={styles.icon}>
            🩺
          </div>

          <h1 style={styles.title}>
            Diabetes Prediction System
          </h1>

          <p style={styles.subtitle}>
            AI-powered health risk prediction
          </p>

        </div>

        <form onSubmit={handleSubmit}>

          {Object.keys(formData).map((key) => (

            <div key={key} style={styles.inputGroup}>

              <label style={styles.label}>
                {key}
              </label>

              <input

                type="number"

                step="any"

                name={key}

                placeholder={`Enter ${key}`}

                value={formData[key]}

                onChange={handleChange}

                required

                style={styles.input}

              />

            </div>

          ))}

          <button
            type="submit"
            style={styles.button}
          >

            {loading ? "Predicting..." : "Predict Diabetes"}

          </button>

        </form>

        {result && (

          <div style={styles.resultBox}>

            <h2 style={styles.resultText}>
              {result}
            </h2>

            <p style={styles.confidence}>
              Confidence: {confidence}%
            </p>

          </div>

        )}

      </div>

    </div>
  );
}

const styles = {

  container: {

    minHeight: "100vh",

    display: "flex",

    justifyContent: "center",

    alignItems: "center",

    background:
      "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)",

    position: "relative",

    overflow: "hidden",

    padding: "20px"
  },

  overlay: {

    position: "absolute",

    width: "100%",

    height: "100%",

    background:
      "rgba(255,255,255,0.03)",

    backdropFilter: "blur(2px)"
  },

  card: {

    position: "relative",

    zIndex: 10,

    width: "100%",

    maxWidth: "500px",

    padding: "35px",

    borderRadius: "20px",

    background:
      "rgba(255,255,255,0.12)",

    backdropFilter: "blur(12px)",

    border:
      "1px solid rgba(255,255,255,0.2)",

    boxShadow:
      "0 8px 32px rgba(0,0,0,0.3)"
  },

  header: {

    textAlign: "center",

    marginBottom: "25px"
  },

  icon: {

    fontSize: "50px",

    marginBottom: "10px"
  },

  title: {

    color: "white",

    fontSize: "32px",

    fontWeight: "700",

    marginBottom: "10px",

    letterSpacing: "1px"
  },

  subtitle: {

    color: "#dfe9f3",

    fontSize: "15px"
  },

  inputGroup: {

    marginBottom: "18px"
  },

  label: {

    display: "block",

    marginBottom: "8px",

    color: "white",

    fontWeight: "500",

    fontSize: "14px"
  },

  input: {

    width: "100%",

    padding: "14px",

    borderRadius: "10px",

    border: "none",

    outline: "none",

    fontSize: "15px",

    background:
      "rgba(255,255,255,0.18)",

    color: "white",

    backdropFilter: "blur(5px)",

    boxSizing: "border-box"
  },

  button: {

    width: "100%",

    padding: "15px",

    marginTop: "10px",

    border: "none",

    borderRadius: "12px",

    background:
      "linear-gradient(135deg,#00c6ff,#0072ff)",

    color: "white",

    fontSize: "17px",

    fontWeight: "600",

    cursor: "pointer",

    transition: "0.3s"
  },

  resultBox: {

    marginTop: "25px",

    padding: "20px",

    borderRadius: "15px",

    background:
      "rgba(255,255,255,0.15)",

    textAlign: "center",

    animation: "fadeIn 0.5s ease"
  },

  resultText: {

    color: "#ffffff",

    marginBottom: "10px"
  },

  confidence: {

    color: "#dfe9f3",

    fontSize: "16px"
  }
};

export default App;