import React from "react";
import { GoogleLogin } from "@react-oauth/google";
import axios from "axios";

const clientID =
  "445686815285-see1e6s9758d5iudh9q8l29137dmoou0.apps.googleusercontent.com";

function LoginButton() {
  const onSuccess = (res) => {
    console.log("LOGIN SUCCESS! Current user: ", res.profileObj);
    axios
      .post("/login", { token: res.credential })
      .then((response) => console.log(response.data))
      .catch((error) => console.log(error));
  };

  const onFailure = (res) => {
    console.log("LOGIN Failed! res: ", res);
  };

  return (
    <div id="signInButton">
     <GoogleLogin
        clientId={clientID}
        buttonText="Login"
        onSuccess={onSuccess}
        onFailure={onFailure}
        cookiePolicy={"single_host_origin"}
        isSignedIn={true}
      />
    
    </div>
  );
}

export default LoginButton;
