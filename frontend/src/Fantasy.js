import React, { useEffect, useState } from "react";
import Loader from "./components/Loading";

// Fix the fantasy thing, looks like its giving some constructors unreasonable points

function Fantasy() {
  const [data, setData] = useState({});
  const [selectedRace, setSelectedRace] = useState("");

  useEffect(() => {
    if (selectedRace !== "") {
      fetch("/fantasy", {
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

  const getConstructorImage = (constructorName) => {
    const fileName =
      constructorName.toLowerCase().replace(/[^a-z]/g, "") + ".avif";
    return `./constructors/${fileName}`;
  };

  return (
    <div>
      <h1>Fantasy page</h1>
      <p>This is the Fantasy page</p>

      <form action="#" method="post">
        <select
          name="race"
          id="race"
          onChange={(e) => setSelectedRace(e.target.value)}
          defaultValue=""
        >
          <option value="" disabled="disabled">
            Select a race
          </option>
          <option value="bahrain_grand_prix">Bahrain Grand Prix</option>
          <option value="saudi arabian_grand_prix">
            Saudi Arabian Grand Prix
          </option>
          <option value="australian_grand_prix">Australian Grand Prix</option>
          <option value="japanese_grand_prix">Japanese Grand Prix</option>
          <option value="chinese_grand_prix">Chinese Grand Prix</option>
          <option value="miami_grand_prix">Miami Grand Prix</option>
          <option value="emilia romagna_grand_prix">
            Emilia-Romagna Grand Prix
          </option>
          <option value="monaco_grand_prix">Monaco Grand Prix</option>
          <option value="canadian_grand_prix">Canadian Grand Prix</option>
          <option value="spanish_grand_prix">Spanish Grand Prix</option>
          <option value="austrian_grand_prix">Austrian Grand Prix</option>
          <option value="british_grand_prix">British Grand Prix</option>
          <option value="belgian_grand_prix">Belgian Grand Prix</option>
          <option value="dutch_grand_prix">Dutch Grand Prix</option>
          <option value="italian_grand_prix">Italian Grand Prix</option>
          <option value="azerbaijan_grand_prix">Azerbaijan Grand Prix</option>
          {/* <option value="saudi_arabian_grand_prix">Singapore Grand Prix</option> */}
          <option value="united states_grand_prix">
            United States Grand Prix
          </option>
          {/* <option value="mexican_grand_prix">Mexican Grand Prix</option> */}
          <option value="brazilian_grand_prix">Brazilian Grand Prix</option>
          <option value="las vegas_grand_prix">Las Vegas Grand Prix</option>
          <option value="qatar_grand_prix">Qatar Grand Prix</option>
          <option value="abu dhabi_grand_prix">Abu Dhabi Grand Prix</option>
        </select>
      </form>

      {data && data.drivers && data.constructors ? (
        <div>
          <h1>Drivers:</h1>

          {data.drivers.map((drivers, idx) => (
            <div key={idx}>
              <img
                src={getDriverImage(drivers[0])}
                alt={drivers[0]}
                className="driver-image"
                draggable="false"
              ></img>
              <p>
                {drivers[0]}, Price: {drivers[1]}, Extimated Points:{" "}
                {drivers[2]}
              </p>
            </div>
          ))}

          <h1>Constructors:</h1>

          {data.constructors.map((constructors, idx) => (
            <div key={idx}>
              <img
                src={getConstructorImage(constructors[0])}
                alt={constructors[0]}
                className="constructor-image"
                draggable="false"
              ></img>
              <p>
                {constructors[0]}, Price: {constructors[1]}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <Loader />
      )}
    </div>
  );
}

export default Fantasy;
