import React, { useEffect, useState } from "react";
import "./Home.css";

function Home() {
  const [imageIndex, setImageIndex] = useState(0);
  const backgrounds = [
    "./backgrounds/bg.jpg",
    "./backgrounds/sunset.jpg",
    "./backgrounds/mclaren.jpg",
    "./backgrounds/mercedes.jpg",
    "./backgrounds/ferrari2.jpg",
    "./backgrounds/ferrari3.jpg",
    "./backgrounds/williams2.jpg",
    "./backgrounds/merc2.jpg",
  ];

  useEffect(() => {
    const changeBackground = () => {
      setImageIndex((prevIndex) => (prevIndex + 1) % backgrounds.length);
    };

    const intervalId = setInterval(changeBackground, 15000);

    return () => clearInterval(intervalId);
  }, [backgrounds.length]);

  return (
    <div className="outer">
      <div className="header-container">
        <header>
          <h1>Welcome to GridMaster</h1>
          <p>Your one pit-stop destination for Formula 1 Predictions</p>
        </header>
        <div className="home-container">
          {backgrounds.map((bg, index) => (
            <img
              key={index}
              className={`home ${index === imageIndex ? "showing" : ""}`}
              src={bg}
              alt={`Background ${index + 1}`}
            />
          ))}
        </div>
      </div>

      <div className="home-content">
        <section className="about">
          <h2 className="about-header">About</h2>
          <p className="about-text">
            GridMaster is a Formula 1 prediction application aimed at helping F1
            fanatics accurately determine the finishing grid at any F1 race and
            to develop optimal fantasy teams to get one over on their friends!
          </p>
        </section>
        <section className="goals">
          <h2 className="goals-header">Behind the UI</h2>
          <p className="goals-text">
            GridMaster leverages advanced technologies to provide accurate
            Formula 1 predictions and optimal fantasy teams. We use Python web
            scrapers to collect race data, the XGBoost machine learning model
            for predictions, and both MongoDB and PostgreSQL for data storage.
            Our backend is powered by Flask, while React and Chart.js create a
            dynamic and responsive frontend.
          </p>
        </section>
        <section className="story">
          <h2 className="story-header">The Story</h2>
          <p className="story-text">
            As an ardent F1 fan, I was curious about the possibility of
            developing a model that was accurate enough to predict the results
            of my favorite sport. As an incoming computer science sophmore, I
            wanted to learn more about different technologies as possible to
            expand my knowledge-base.
          </p>
        </section>
      </div>
    </div>
  );
}

export default Home;
