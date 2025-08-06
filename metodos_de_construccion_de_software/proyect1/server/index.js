const express = require('express');
const cors =require('cors');
require('dotenv').config();


const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());


app.get('/api/hello' , (req, res) => {
    res.json({message: 'Hola te escribo desde Nodejs en el backend' });
});

app.listen(PORT, () => {
    console.log( `servidor backend corriendo en http://localhost:${ PORT}` );
});

