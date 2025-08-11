const mysql = require('mysql2');
require('dotenv').config();

const connection = mysql.createConnection({
    host: process.env.DB_HOST,        
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});

// SQL para crear la tabla si no existe
const createTableSQL = `
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    pais VARCHAR(50) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    anios INT NOT NULL
)`;

connection.connect((err) => {
    if (err) {
        console.error('Error al conectar la base de datos:', err);
        process.exit(1);
    }
    console.log('Conexión exitosa a la base de datos.');
    
    // Crear la tabla
    connection.query(createTableSQL, (err, result) => {
        if (err) {
            console.error('Error al crear la tabla:', err);
        } else {
            console.log('Tabla empleados verificada/creada correctamente.');
        }
        
        connection.end();
        process.exit(0);
    });
});
