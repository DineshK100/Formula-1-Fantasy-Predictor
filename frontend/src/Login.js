import React, { useState } from "react";
import { useAuth } from "./Auth"; 
import { useNavigate } from 'react-router-dom';

function Login() {
    const { login } = useAuth();
    const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("Login successful!");
        login(data.token);
        navigate("/");
      } else {
        alert("Login failed: " + data.message);
      }
    })
    .catch((error) => {
      console.error("There was an error!", error);
      alert("Login failed: " + error.message);
    });
  };

  return (
    <div className="signup-wrapper">
      <div className="mask d-flex align-items-center justify-content-center gradient-custom-3">
        <div className="signup-container">
          <div className="card" style={{ borderRadius: "15px" }}>
            <div className="card-body p-5">
              <h2 className="text-uppercase text-center mb-5" style={{ color: "black" }}>Login</h2>
              <form onSubmit={handleSubmit}>
                <div data-mdb-input-init className="form-outline mb-4">
                  <input name="username" type="text" id="form3Example1cg" className="form-control form-control-lg border border-dark" value={formData.username} onChange={handleChange} required/>
                  <label className="form-label" htmlFor="form3Example1cg">Username</label>
                </div>
                <div data-mdb-input-init className="form-outline mb-4">
                  <input name="password" type="password" id="form3Example4cg" className="form-control form-control-lg border border-dark" value={formData.password} onChange={handleChange} required />
                  <label className="form-label" htmlFor="form3Example4cg">Password</label>
                </div>
                <div className="d-flex justify-content-center">
                  <button type="submit" className="btn btn-success btn-block btn-lg gradient-custom-4 text-body">Submit</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
