import React from "react";
import "./Loading.css";

function Loader() {
  return (
    <div className = "loading-icon">
      <img src="loading.png" alt = "loading" className="spinner" />
    </div>
  );
}

export default Loader;
