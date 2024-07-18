import React, { useEffect, useState } from "react";
import Loader from "./components/Loading";
import "./Predict.css";

function Predict() {
  const [data, setData] = useState({});
  const [selectedRace, setSelectedRace] = useState("");

  useEffect(() => {
    if (selectedRace !== "") {
      fetch("/predict", {
        method: "POST",
        body: JSON.stringify({ race: selectedRace }),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          setData(data);
          console.log(data);
        })
        .catch((error) => console.error("Error fetching predictions:", error));
    }
  }, [selectedRace]);

  const getDriverImage = (driverName) => {
    driverName = driverName.replace("ü", "u");
    driverName = driverName.replace("é", "e");
    const fileName = driverName.toLowerCase().replace(/[^a-z]/g, "") + ".avif";
    return `./drivers/${fileName}`;
  };

  return (
    <div>
      <h1>Prediction page</h1>

      <form action="#" method="post" >
        <select name = "race" id="race" onChange={(e) => setSelectedRace(e.target.value)}>
          <option value="" disabled="disabled">
            Select a race
          </option>
          <option value="british_grand_prix">British Grand Prix</option>
          <option value="austrian_grand_prix">Austrian Grand Prix</option>
          <option value="australian_grand_prix">British Grand Prix</option>
          <option value="hungary_grand_prix">Austrian Grand Prix</option>
          <option value="bahrain_grand_prix">British Grand Prix</option>
          <option value="saudi_arabian_grand_prix">Austrian Grand Prix</option>
          <option value="british_grand_prix">British Grand Prix</option>
          <option value="austrian_grand_prix">Austrian Grand Prix</option>

        </select>
      </form>

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

                {index < 3 ? (
                  <td>
                    <img
                      src={getDriverImage(item.Driver)}
                      alt={item.Driver}
                      className="driver-image"
                      draggable="false"
                    ></img>
                    <td>{item.Driver}</td>
                  </td>
                ) : (
                  <td>{item.Driver}</td>
                )}

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
