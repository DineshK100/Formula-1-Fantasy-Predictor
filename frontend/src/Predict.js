import React, { useEffect, useState } from "react";
import Loader from "./components/Loading";
import './Predict.css'

function Predict() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState({});

  useEffect(() => {
    fetch("/predict")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setLoading(false);
        console.log(data);
      });
  }, []);

  const getDriverImage = (driverName) => {

    driverName = driverName.replace("ü", "u");
    driverName = driverName.replace("é", "e");

    const fileName = driverName.toLowerCase().replace(/[^a-z]/g, "", '') + ".avif";
    return `./drivers/${fileName}`;
  };

  return (
    <div>
      <h1>Prediction page</h1>
      {data.length ? (
        <table className="podium table">
          <thead>
            <tr>
              <th>Position</th>
              <th>Driver</th>
              <th>Constructor</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{item.Predicted_Position}</td>

                <td>
                  <img
                    src={getDriverImage(item.Driver)}
                    //alt={item.Driver}
                    className="driver-image"
                  ></img>
                </td>
                <td>{item.Constructor}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <Loader className="spinning" />
      )}
    </div>
  );
}

export default Predict;