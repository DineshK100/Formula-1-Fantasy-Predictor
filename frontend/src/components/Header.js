import React, { useEffect, useState } from "react";
import "./Header.css"; // Assuming you have custom styles

const Header = () => {
  useEffect(() => {
    const handleScroll = () => {
      const navEl = document.querySelector(".navbar");
      if (window.scrollY >= 56) {
        navEl.classList.add("navbar-scrolled");
      } else {
        navEl.classList.remove("navbar-scrolled");
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);
  
  return (
    <>
      <img className="bg-image" src="bg.jpg" alt="Background" />
        <nav class="navbar navbar-expand-sm navbar-dark fixed-top">
          <div className="container">
            <a class="navbar-brand" href="/">
              GridMaster
            </a>
            <button
              class="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav">
                <li class="nav-item active">
                  <a class="nav-link" href="/">
                    Stats
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/fantasy">
                    Fantasy
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/predict">
                    Predict
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/signup">
                    Sign Up
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
    </>
  );
};

export default Header;
