import React, { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import Loader from "./components/Loading/Loading";
import "./styles/Predict.css";

// Make it look like the formula 1 selector grid
// Then when one is selected the Loading icon shows up and then animation to show the positions
// Have two view options
// covert to json

const races = [
  {
    id: "bahrain_grand_prix",
    name: "Bahrain Grand Prix",
    country: "Bahrain",
    image: "./tracks/bahrain.png",
  },
  {
    id: "saudi arabian_grand_prix",
    name: "Saudi Arabian Grand Prix",
    country: "Saudi Arabia",
    image: "./tracks/saudi.png",
  },
  {
    id: "australian_grand_prix",
    name: "Australia Grand Prix",
    country: "Australia",
    image: "./tracks/australia.png",
  },
  {
    id: "japanese_grand_prix",
    name: "Japanese Grand Prix",
    country: "Japan",
    image: "./tracks/japan.png",
  },
  {
    id: "chinese_grand_prix",
    name: "Chinese Grand Prix",
    country: "Japan",
    image: "./tracks/china.png",
  },
  {
    id: "miami_grand_prix",
    name: "Miami Grand Prix",
    country: "United States",
    image: "./tracks/miami.png",
  },
  {
    id: "emilia romagna_grand_prix",
    name: "Emilia-Romagna Grand Prix",
    country: "Spain",
    image: "./tracks/emilia.png",
  },
  {
    id: "monaco_grand_prix",
    name: "Monaco Grand Prix",
    country: "Monaco",
    image: "./tracks/monaco.png",
  },
  {
    id: "canadian_grand_prix",
    name: "Canadian Grand Prix",
    country: "Canada",
    image: "./tracks/canada.png",
  },
  {
    id: "spanish_grand_prix",
    name: "Spanish Grand Prix",
    country: "Spain",
    image: "./tracks/spain.png",
  },
  {
    id: "austrian_grand_prix",
    name: "Austrian Grand Prix",
    country: "Austria",
    image: "./tracks/austria.png",
  },
  {
    id: "british_grand_prix",
    name: "British Grand Prix",
    country: "United Kingdon",
    image: "./tracks/british.png",
  },
  {
    id: "belgian_grand_prix",
    name: "Belgian Grand Prix",
    country: "Beligum",
    image: "./tracks/belgium.avif",
  },
  {
    id: "dutch_grand_prix",
    name: "Dutch Grand Prix",
    country: "Netherlands",
    image: "./tracks/dutch.avif",
  },
  {
    id: "italian_grand_prix",
    name: "Italian Grand Prix",
    country: "Italian",
    image: "./tracks/italy.avif",
  },
  {
    id: "azerbaijan_grand_prix",
    name: "Azerbaijan Grand Prix",
    country: "Azerbaijan",
    image: "./tracks/azerbaijan.avif",
  },
  {
    id: "united states_grand_prix",
    name: "United States Grand Prix",
    country: "United States",
    image: "./tracks/usa.avif",
  },
  {
    id: "brazilian_grand_prix",
    name: "Brazilian Grand Prix",
    country: "Brazil",
    image: "./tracks/brazil.avif",
  },
  {
    id: "las_vegas_grand_prix",
    name: "Las Vegas Grand Prix",
    country: "United States",
    image: "./tracks/vegas.avif",
  },
  {
    id: "qatar_grand_prix",
    name: "Qatar Grand Prix",
    country: "Qatar",
    image: "./tracks/qatar.avif",
  },
  {
    id: "abu dhabi_grand_prix",
    name: "Abu Dhabi Grand Prix",
    country: "Abu Dhabi",
    image: "./tracks/abudhabi.avif",
  },
];

function Predict() {
  const [toggle, setIsToggle] = useState(false);
  const [data, setData] = useState([]);
  const [selectedRace, setSelectedRace] = useState("");
  const [shouldLoad, setShouldLoad] = useState(false);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    if (selectedRace !== "") {
      setShouldLoad(true);
      setHasError(false);
      
      fetch("/predict", {
        method: "POST",
        body: JSON.stringify({ race: selectedRace }),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error('Network response was not ok');
          }
          return res.json();
        })
        .then((data) => {
          setData(data);
          setShouldLoad(false);
        })
        .catch((error) => {
          console.error("Error fetching predictions:", error);
          setShouldLoad(false);
          setHasError(true);
          alert("Error loading this prediction, try another one!");
        });
    }
  }, [selectedRace]);

  const getDriverImage = (driverName) => {
    driverName = driverName.replace("ü", "u");
    driverName = driverName.replace("é", "e");
    const fileName = driverName.toLowerCase().replace(/[^a-z]/g, "") + ".avif";
    return `./drivers/${fileName}`;
  };

  const handleRaceSelect = (raceId) => {
    setData([]); 
    setSelectedRace(raceId);
    setIsToggle(true);
    setShouldLoad(true);
    setHasError(false); // Reset error state on new race selection
  };

  return (
    <div>
      <div className="top">
        <h1 className="main-text">Driver Predictions</h1>
        <p className="sub-text">Select a race to predict</p>
      </div>

      {(!toggle && !hasError) ? (
        <div className="race-grid">
          {races.map((race) => (
            <div
              key={race.id}
              className={`race-card`}
              onClick={() => handleRaceSelect(race.id)}
            >
              <div className="race-header">
                <span className="country">{race.country}</span>
              </div>
              <hr />
              <div className="race-body">
                <div className="race-info">
                  <p className="race-name">{race.name}</p>
                </div>
                <hr />
                <img src={race.image} alt={race.name} className="track-image" />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="main-content">
          <Sidebar onRaceSelect={handleRaceSelect} className="sidebar" />
          <div className="predictions">
            {shouldLoad && !hasError && data.length === 0 ? (
              <Loader />
            ) : (
              <div className="predictions-grid">
                {data.map((item, index) => (
                  <div className="backboard" key={index}>
                    <img
                      src={getDriverImage(item.Driver)}
                      alt={item.Driver}
                      className="driver-image"
                      draggable="false"
                    />
                    <div className="backboard-content">
                      <h2 className="driver-name">{item.Driver}</h2>
                      <p>{item.Constructor}</p>
                      <p>Position: {item.Predicted_Position}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Predict;