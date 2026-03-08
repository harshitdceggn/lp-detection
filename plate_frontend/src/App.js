import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

const [file, setFile] = useState(null);
const [preview, setPreview] = useState(null);
const [result, setResult] = useState("");
const [loading, setLoading] = useState(false);

const handleUpload = (e) => {
const img = e.target.files[0];
setFile(img);
setPreview(URL.createObjectURL(img));
setResult("");
};

const predict = async () => {

```
if (!file) {
  alert("Upload image first");
  return;
}

const formData = new FormData();
formData.append("file", file);

try {

  setLoading(true);

  const res = await axios.post(
    "https://lp-detection.onrender.com/predict/",
    formData
  );

  setResult(res.data.plate_number);

} catch (error) {

  console.error(error);
  alert("Prediction failed");

} finally {
  setLoading(false);
}
```

};

return ( <div className="app">

```
  <h1 className="title">
    LICENSE PLATE DETECTION
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
        Upload Image
      </p>

    </div>


    {/* PREDICT BUTTON */}
    <div className="predict-container">

      <button
        className="predict-btn"
        onClick={predict}
        disabled={loading}
      >
        {loading ? "Processing..." : "Predict"}
      </button>

    </div>


    {/* RESULT PANEL */}
    <div className="panel result">

      <p className="panel-text">
        Results
      </p>

      <h2 className="plate-result">
        {result}
      </h2>

    </div>

  </div>

</div>
```

);
}

export default App;
