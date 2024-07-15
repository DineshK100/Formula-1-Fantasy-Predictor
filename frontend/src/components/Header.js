import React from "react";
import './Header.css'

const Header = () => {
  return (
    
    <header className="header">

      <h1 className="logo">Tempo</h1>

      <div className = "line bottom"></div>
      <div className = "line diagnol"></div>
      <div className = "line top"></div>


      <nav className="navbar">
        <ul>
          <li>
            <a href="/predict">Predict</a>
          </li>
          <li>
            <a href="/fantasy">Fantasy</a>
          </li>
          <li>
            <a href="/signup">Sign Up</a>
          </li>
        </ul>
      </nav>

    </header>
  );
};

export default Header;
