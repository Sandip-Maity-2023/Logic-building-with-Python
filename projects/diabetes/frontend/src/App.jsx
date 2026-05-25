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

        "http://127.0.0.1:5000/predict",

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

      <div style={styles.card}>

        <h1 style={styles.title}>
          Diabetes Prediction System
        </h1>

        <form onSubmit={handleSubmit}>

          {Object.keys(formData).map((key) => (

            <div key={key} style={styles.inputGroup}>

              <input

                type="number"

                step="any"

                name={key}

                placeholder={key}

                value={formData[key]}

                onChange={handleChange}

                required

                style={styles.input}

              />

            </div>

          ))}

          <button type="submit" style={styles.button}>

            {loading ? "Predicting..." : "Predict"}

          </button>

        </form>

        {result && (

          <div style={styles.resultBox}>

            <h2>{result}</h2>

            <p>
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

    display: "flex",

    justifyContent: "center",

    alignItems: "center",

    minHeight: "100vh",

    backgroundColor: "#f4f4f4"

  },

  card: {

    backgroundColor: "white",

    padding: "30px",

    borderRadius: "10px",

    width: "400px",

    boxShadow: "0px 0px 10px rgba(0,0,0,0.2)"

  },

  title: {

    textAlign: "center",

    marginBottom: "20px"

  },

  inputGroup: {

    marginBottom: "15px"

  },

  input: {

    width: "100%",

    padding: "10px",

    borderRadius: "5px",

    border: "1px solid #ccc"

  },

  button: {

    width: "100%",

    padding: "12px",

    border: "none",

    borderRadius: "5px",

    backgroundColor: "#007bff",

    color: "white",

    fontSize: "16px",

    cursor: "pointer"

  },

  resultBox: {

    marginTop: "20px",

    textAlign: "center"

  }
};

export default App;