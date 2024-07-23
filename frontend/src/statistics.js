import { React, useState } from "react";
import "./Statistics.css";

function Statistics() {
  const [statsData, setstatsData] = useState({
    race: "",
    points: "",
  });

  const handleChange = (e) => {
    setstatsData({ ...statsData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {

    const token = localStorage.getItem('token'); // Assuming you store the token in localStorage

    fetch("/stats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(statsData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("successful!");
        } else {
          alert("Failed: " + data.message);
        }
      })
      .catch((error) => {
        console.error("There was an error!", error);
        alert("Failed: " + error.message);
      });
  };

  return (
    <div className="submission-data">
      <form onSubmit={handleSubmit}>
        <input
          name="race"
          type="text"
          id="form3Example1cg"
          className="form-control form-control-lg border border-dark"
          value={statsData.race}
          onChange={handleChange}
          required
        />
        <input
          name="points"
          type="text"
          id="form3Example1cg"
          className="form-control form-control-lg border border-dark"
          value={statsData.points}
          onChange={handleChange}
          required
        />
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
}

export default Statistics;
