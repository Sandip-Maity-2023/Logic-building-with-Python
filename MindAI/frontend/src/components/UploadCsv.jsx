import React, { useRef, useState } from "react";

function UploadCsv({ onUpload, isLoading }) {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [message, setMessage] = useState("");
  const inputRef = useRef(null);

  const acceptFile = (nextFile) => {
    if (!nextFile) return;

    const isCsv =
      nextFile.name.toLowerCase().endsWith(".csv") ||
      nextFile.type === "text/csv" ||
      nextFile.type === "application/vnd.ms-excel";

    if (!isCsv) {
      setMessage("Please choose a valid CSV file.");
      setFile(null);
      return;
    }

    setFile(nextFile);
    setMessage(`${nextFile.name} is ready to upload.`);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setMessage("Select a CSV file before uploading.");
      return;
    }

    setMessage("");
    await onUpload(file);
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">Batch workflow</span>
          <h3>Upload a CSV dataset</h3>
        </div>
        <p>Drop a file, validate it instantly, then send your dataset for recommendation generation.</p>
      </div>

      <form className="panel-form" onSubmit={handleSubmit}>
        <button
          type="button"
          className={`upload-dropzone${isDragging ? " dragging" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(event) => {
            event.preventDefault();
            setIsDragging(false);
            acceptFile(event.dataTransfer.files?.[0]);
          }}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".csv"
            hidden
            onChange={(event) => acceptFile(event.target.files?.[0])}
          />
          <strong>{file ? file.name : "Drag and drop your CSV here"}</strong>
          <span>{file ? "Click to replace the file" : "or click to browse from your device"}</span>
        </button>

        <div className="helper-grid">
          <div className="helper-card">
            <span>Expected fields</span>
            <strong>restaurant_name, cuisine, rating, sentiment_score</strong>
          </div>
          <div className="helper-card">
            <span>Why upload?</span>
            <strong>Analyze multiple restaurants in a single run.</strong>
          </div>
        </div>

        {message ? <div className="inline-message">{message}</div> : null}

        <div className="panel-actions">
          <button type="submit" className="primary-button" disabled={isLoading || !file}>
            {isLoading ? "Uploading..." : "Upload and analyze"}
          </button>
          <button
            type="button"
            className="ghost-button"
            onClick={() => {
              setFile(null);
              setMessage("");
              if (inputRef.current) {
                inputRef.current.value = "";
              }
            }}
          >
            Remove file
          </button>
        </div>
      </form>
    </section>
  );
}

export default UploadCsv;
