import React, { useEffect, useState } from "react";

function Fantasy() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch("/fantasy")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      })

      .catch((error) => console.log(error));
  }, []);
  return (
    <div>
      <h1>Fantasy page</h1>
      <p>This is the Fantasy page</p>

      
    </div>
  );
}

export default Fantasy;
