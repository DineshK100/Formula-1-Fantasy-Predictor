import React, { useEffect, useState } from "react";
import "./Loading.css";

function Loader() {
  return (
    <div className = "loading-icon">
      <img src="loading.png" className="spinner" />
    </div>
  );
}

export default Loader;
