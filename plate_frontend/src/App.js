import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState("");

  const handleUpload = (e) => {
    const img = e.target.files[0];
    setFile(img);
    setPreview(URL.createObjectURL(img));
  };

  const predict = async () => {

    if (!file) {
      alert("Upload image first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8000/predict/",
      formData
    );

    setResult(res.data.plate_number);
  };

  return (
    <div className="app">

      <h1 className="title">
        LISCENSE PLATE DETECTION
      </h1>

      <div className="main-container">

        {/* LEFT PANEL */}
        <div className="panel upload">

          <input
            type="file"
            onChange={handleUpload}
          />

          {preview && (
            <img
              src={preview}
              alt="preview"
              className="preview"
            />
          )}

          <p className="panel-text">
            upload image
          </p>

        </div>


        {/* PREDICT BUTTON */}
        <div className="predict-container">

          <button
            className="predict-btn"
            onClick={predict}
          >
            predict
          </button>

        </div>


        {/* RESULT PANEL */}
        <div className="panel result">

          <p className="panel-text">
            results
          </p>

          <h2 className="plate-result">
            {result}
          </h2>

        </div>

      </div>

    </div>
  );
}

export default App;