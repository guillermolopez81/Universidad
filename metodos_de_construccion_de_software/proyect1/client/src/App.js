import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMensaje] = useState('');

  useEffect(() => {
    axios.get('/api/hello') // usamos proxy
      .then(res => setMensaje(res.data.mensaje))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>APLICACIÓN CON REACTJS Y NODE JS</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;