import React from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./Home";
import Predict from "./Predict";
import SignUp from "./SignUp";
import Fantasy from "./Fantasy";
import Header from "./components/Header";
import Statistics from "./statistics";

function App() {

  return (
    <>
      <Header />

      <div className="container">

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/fantasy" element={<Fantasy />} />
          <Route path="/signup" element={<SignUp />} />
          {/* <Route path="/statistics" element={<Statistics />} /> */}
        </Routes>
        
      </div>
    </>
  );
}

export default App;
