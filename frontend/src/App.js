import React from 'react';
import { Route, Routes} from 'react-router-dom'
import Home from './Home';

function App() {
  // const [data, setData] = useState({});

  // useEffect(() => {
  //   fetch("/predict")
  //     .then(res => {
  //       return res.json();
  //     })
  //     .then(data => {
  //       setData(data);
  //       console.log(data);
  //     })

  // }, []);

  return ( 
  <Routes>
    <Route path = "/" element = {<Home/> } />
  </Routes>

  );
}

export default App;
