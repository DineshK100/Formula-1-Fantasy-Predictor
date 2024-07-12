import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch("/predict")
      .then(res => {
        
        return res.json();
      })
      .then(data => {
        setData(data);
        console.log(data);
      })

  }, []);

  return (
    <div>
     
    </div>
  );
}

export default App;
