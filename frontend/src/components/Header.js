import React, { useEffect } from "react";
import "./Header.css";
import { useAuth } from "../Auth"; // Ensure the correct import path

// I like the idea of putting the design things to the header elements as well
const Header = () => {
  const { isAuthenticated, username, logout } = useAuth();

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
      <nav className="navbar navbar-expand-lg navbar-dark fixed-top">
        <div className="container">
          <div className="left-div navbar-collapse collapse w-100 order-1 order-md-0 dual-collapse2">
            <ul className="navbar-nav me-auto custom-padding">
              <li className="nav-item">
                <a className="nav-link" href="/fantasy">
                  Fantasy
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/predict">
                  Predict
                </a>
              </li>
            </ul>
          </div>
          <div className="mx-auto order-0">
            <a className="navbar-brand mx-auto formula" href="/">
              GridMaster
            </a>
            <button
              className="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target=".dual-collapse2"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
          </div>
          <div className="right-div navbar-collapse collapse w-100 order-3 dual-collapse2">
            <ul className="navbar-nav ms-auto custom-padding">
              <li className="nav-item">
                <a className="nav-link" href="/stats">
                  Statistics
                </a>
              </li>
              {isAuthenticated ? (
                <li className="nav-item dropdown">
                  <a className="nav-link">Hello, {username}</a>
                  <div className="dropdown-content">
                    <a onClick={logout}>Sign Out</a>
                  </div>
                </li>
              ) : (
                <li className="nav-item">
                  <a className="nav-link" href="/signup">
                    Login
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Header;
