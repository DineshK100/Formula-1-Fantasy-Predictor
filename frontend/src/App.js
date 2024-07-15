import React from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./Home";
import Predict from "./Predict";
import SignUp from "./SignUp";
import Fantasy from "./Fantasy";

import Header from "./components/Header";

function App() {
  // const [data, setData] = useState({});

  // useEffect(() => {
  //   fetch("/predict")
  //     .then(res => {
  //       return res.json();
  //     })
  //     .then(data => {
  //       setData(data);
  //       console.log(data);
  //     })

  // }, []);

  return (
    <>
      <Header />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/fantasy" element={<Fantasy />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
