import React, { useState } from "react";
import { useAuth } from "./Auth";
import "./Signup.css";
import { useNavigate } from "react-router-dom";

function SignUp() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Sign up successful!");
          login(data.token);
          navigate("/");
        } else {
          alert("Sign up failed: " + data.message);
        }
      })
      .catch((error) => {
        console.error("There was an error!", error);
        alert("Sign up failed: " + error.message);
      });
  };

  return (
    <div className="signup-wrapper">
      <div className="mask d-flex align-items-center justify-content-center gradient-custom-3">
        <div className="signup-container">
          <div className="card" style={{ borderRadius: "15px" }}>
            <div className="card-body p-5">
              <h2
                className="text-uppercase text-center mb-5"
                style={{ color: "black" }}
              >
                Create an account
              </h2>
              <form onSubmit={handleSubmit}>
                <div data-mdb-input-init className="form-outline mb-4">
                  <input
                    name="username"
                    type="text"
                    id="form3Example1cg"
                    className="form-control form-control-lg border border-dark"
                    value={formData.username}
                    onChange={handleChange}
                    required
                  />
                  <label className="form-label" htmlFor="form3Example1cg">
                    Username
                  </label>
                </div>
                <div data-mdb-input-init className="form-outline mb-4">
                  <input
                    name="password"
                    type="password"
                    id="form3Example4cg"
                    className="form-control form-control-lg border border-dark"
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                  <label className="form-label" htmlFor="form3Example4cg">
                    Password
                  </label>
                </div>
                <div data-mdb-input-init className="form-outline mb-4">
                  <input
                    name="confirmPassword"
                    type="password"
                    id="form3Example4cdg"
                    className="form-control form-control-lg border border-dark"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                  />
                  <label className="form-label" htmlFor="form3Example4cdg">
                    Re-enter password
                  </label>
                </div>
                <div className="d-flex justify-content-center">
                  <button
                    type="submit"
                    className="btn btn-success btn-block btn-lg gradient-custom-4 text-body"
                  >
                    Register
                  </button>
                </div>
                <p className="text-center text-muted mt-5 mb-0">
                  Have already an account?{" "}
                  <a href="/login" className="text-body">
                    <u>Login here</u>
                  </a>
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignUp;
