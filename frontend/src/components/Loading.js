import React from "react";
import "./Loading.css";

function Loader() {
  return (
    <div className="loading-overlay">
      <div className="loading-icon">
        <div className="loading-image">
          <img src="loading.png" alt="loading" className="spinner" />
        </div>
        <div className="loading-header">
          <h1>Loading</h1>
        </div>
        <div className="loading-text">
          <span className="load-bubbles"></span>
          <span className="load-bubbles"></span>
          <span className="load-bubbles"></span>
        </div>
      </div>
    </div>
  );
}

export default Loader;
