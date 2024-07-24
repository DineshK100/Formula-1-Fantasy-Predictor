import React, { useState, useEffect, useRef } from "react";
import { Chart, registerables } from "chart.js";
import "./Statistics.css";
import { useAuth } from "./Auth"; // Ensure the correct import path

// Register all necessary Chart.js components
Chart.register(...registerables);

function Statistics() {
  const [statsData, setStatsData] = useState({ race: "", points: "" });
  const [chartData, setChartData] = useState(null);
  const chartRef = useRef(null);
  const { isAuthenticated } = useAuth();

  const handleChange = (e) => {
    setStatsData({ ...statsData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    fetch("/stats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(statsData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("successful!");
          processChartData(data.stats);
        } else {
          alert("Failed: " + data.message);
        }
      })
      .catch((error) => {
        console.error("There was an error!", error);
        alert("Failed: " + error.message);
      });
  };

  const processChartData = (stats) => {
    const labels = stats.map((stat) => stat.race);
    const dataPoints = stats.map((stat) => stat.points);

    const data = {
      labels: labels,
      datasets: [
        {
          type: "bar",
          label: "Points per Race (Bar)",
          data: dataPoints,
          backgroundColor: "rgba(75, 192, 192, 0.5)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
        {
          type: "line",
          label: "Points per Race (Line)",
          data: dataPoints,
          fill: false,
          backgroundColor: "rgba(153, 102, 255, 0.5)",
          borderColor: "rgba(153, 102, 255, 1)",
        },
      ],
    };

    setChartData(data);
  };

  useEffect(() => {
    if (isAuthenticated) {
      const fetchInitialData = () => {
        const token = localStorage.getItem("token");

        fetch("/stats", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              processChartData(data.stats);
            } else {
              alert("Failed: " + data.message);
            }
          })
          .catch((error) => {
            console.error("There was an error!", error);
            alert("Failed: " + error.message);
          });
      };

      fetchInitialData();
    } else {
      const data = {
        labels: [],
        datasets: [
          {
            type: "bar",
            label: "Points per Race (Bar)",
            data: [],
            backgroundColor: "rgba(75, 192, 192, 0.5)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          },
          {
            type: "line",
            label: "Points per Race (Line)",
            data: [],
            fill: false,
            backgroundColor: "rgba(153, 102, 255, 0.5)",
            borderColor: "rgba(153, 102, 255, 1)",
          },
        ],
      };

      setChartData(data);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (chartData && chartRef.current) {
      const chartInstance = new Chart(chartRef.current, {
        type: "bar",
        data: chartData,
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });

      return () => {
        chartInstance.destroy();
      };
    }
  }, [chartData]);

  return (
    <div className="submission-data">
      <div className="title-info">
        <h1 className="log-header">Personal Fantasy Points Log</h1>
        <p className="info-para">
          Type in the race you want to log as well as the corresponding points,
          and watch how you progress through the season!
        </p>
      </div>
      <div className="chart-container">
        <canvas ref={chartRef} />
      </div>
      {isAuthenticated ? (
        <form onSubmit={handleSubmit} className="form-inputs">
          <div className="input-group">
            <input
              name="race"
              type="text"
              id="form3Example1cg"
              className="form-control form-control-lg border border-dark"
              value={statsData.race}
              onChange={handleChange}
              placeholder="Race Name"
              required
            />
          </div>
          <div className="input-group">
            <input
              name="points"
              type="text"
              id="form3Example1cg"
              className="form-control form-control-lg border border-dark"
              value={statsData.points}
              onChange={handleChange}
              placeholder="Points Scored"
              required
            />
          </div>
          <div>
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
        </form>
      ) : (
        <p>Log in to start logging!</p>
      )}
    </div>
  );
}

export default Statistics;
