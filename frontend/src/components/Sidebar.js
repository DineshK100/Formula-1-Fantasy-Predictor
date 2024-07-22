import { React, useEffect, useState } from "react";

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
    id: "abu_dhabi_grand_prix",
    name: "Abu Dhabi Grand Prix",
    country: "Abu Dhabi",
    image: "./tracks/abudhabi.avif",
  },
];

function Sidebar({ onRaceSelect }) {
  const [selectedRace, setSelectedRace] = useState("");

  const handleRaceSelect = (raceId) => {
    setSelectedRace(raceId);
    onRaceSelect(raceId);
  };

  return (
    <ul className="sidebar">
      <li className="sidebar-header">Select A Race</li>
      {races.map((race) => (
        <li
          className="sidebar-element"
          key={race.id}
          onClick={() => handleRaceSelect(race.id)}
        >
          <span className="name">{race.name}</span>
          <img src={race.image} className="race-image"></img>
        </li>
      ))}
    </ul>
  );
}

export default Sidebar;
