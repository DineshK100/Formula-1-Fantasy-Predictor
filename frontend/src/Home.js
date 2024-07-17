import React, { useEffect, useState } from "react";
import "./Home.css";

function Home() {
  const [imageIndex, setImageIndex] = useState(0);
  const backgrounds = ["./backgrounds/bg.jpg", "./backgrounds/sunset.jpg", "./backgrounds/mclaren.jpg", "./backgrounds/mercedes.jpg", "./backgrounds/ferrari2.jpg", "./backgrounds/ferrari3.jpg", "./backgrounds/williams2.jpg", "./backgrounds/merc2.jpg"];

  useEffect(() => {
    const changeBackground = () => {
      setImageIndex((prevIndex) => (prevIndex + 1) % backgrounds.length);
    };

    const intervalId = setInterval(changeBackground, 15000);

    return () => clearInterval(intervalId);
  }, [backgrounds.length]);

  return (
    <div>
      <header>
        
        <h1>Home page</h1>
        <p>This is the home page</p>

        <div className="backgrounds-container">
          {backgrounds.map((bg, index) => (
            <img
              key={index}
              className={`background ${index === imageIndex ? "showing" : ""}`}
              src={bg}
              alt={`Background ${index + 1}`}
            />
          ))}
        </div>
      </header>

      <div className="extra-content">
        <section>
          <h2>About Us</h2>
          <p>
            We are passionate about motorsport and provide the latest updates
            and predictions on Formula 1 races.
          </p>
        </section>
        <section>
          <h2>Our Services</h2>
          <p>
            We offer detailed statistics, fantasy league integration, and race
            predictions to keep you ahead of the game. Explore our features and
            enhance your Formula 1 experience.
          </p>
        </section>
        <section>
          <h2>Contact Us</h2>
          <p>
            Have any questions or feedback? Feel free to reach out to us. We are
            here to help you with any information you need.
          </p>
        </section>
      </div>
    </div>
  );
}

export default Home;
