import React from "react";

function SignUp() {
  return (
    <div>
      <h1>SignUp page</h1>
      <p>This is the SignUp page</p>

      <section className="vh-100 bg-image">
        <div className="mask d-flex align-items-center h-100 gradient-custom-3">
          <div className="container h-100">
            <div className="row d-flex justify-content-center align-items-center h-100">
              <div className="col-12 col-md-9 col-lg-7 col-xl-6">
                <div className="card" style={{ borderRadius: "15px" }}>
                  <div className="card-body p-5">
                    <h2
                      className="text-uppercase text-center mb-5 "
                      style={{ color: "black" }}
                    >
                      Create an account
                    </h2>

                    <form>
                      <div data-mdb-input-init className="form-outline mb-4">
                        <input
                          type="text"
                          id="form3Example1cg"
                          className="form-control form-control-lg"
                        />
                        <label className="form-label" htmlFor="form3Example1cg">
                          Username
                        </label>
                      </div>

                      <div data-mdb-input-init className="form-outline mb-4">
                        <input
                          type="email"
                          id="form3Example3cg"
                          className="form-control form-control-lg"
                        />
                        <label className="form-label" htmlFor="form3Example3cg">
                          Email
                        </label>
                      </div>

                      <div data-mdb-input-init className="form-outline mb-4">
                        <input
                          type="password"
                          id="form3Example4cg"
                          className="form-control form-control-lg"
                        />
                        <label className="form-label" htmlFor="form3Example4cg">
                          Password
                        </label>
                      </div>

                      <div data-mdb-input-init className="form-outline mb-4">
                        <input
                          type="password"
                          id="form3Example4cdg"
                          className="form-control form-control-lg"
                        />
                        <label
                          className="form-label"
                          htmlFor="form3Example4cdg"
                        >
                          Re-enter password
                        </label>
                      </div>

                      <div className="d-flex justify-content-center">
                        <button
                          type="button"
                          data-mdb-button-init
                          data-mdb-ripple-init
                          className="btn btn-success btn-block btn-lg gradient-custom-4 text-body"
                        >
                          Register
                        </button>
                      </div>

                      <p className="text-center text-muted mt-5 mb-0">
                        Have already an account?{" "}
                        <a href="#!" className="text-body">
                          <u>Login here</u>
                        </a>
                      </p>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default SignUp;
