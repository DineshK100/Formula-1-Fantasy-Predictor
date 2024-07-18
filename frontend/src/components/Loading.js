import React from "react";
import "./Loading.css";

// Need to make it so the Loading... is below and also that the ... do the loading action
// Find a way to make it so that when it is Loading it creates like a new layer and looks like its loading
function Loader() {
  return (
    <div className = "loading-icon">
      <img src="loading.png" alt = "loading" className="spinner" />
      <h1>Loading...</h1>
    </div>
  );
}

export default Loader;
