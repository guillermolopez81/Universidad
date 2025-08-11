const express = require('express');
const cors = require('cors');
const db = require('./db');
const app = express();

app.use(cors());
app.use(express.json());

// GET: Obtener todos los empleados
app.get('/empleados', (req, res) => {
    const sql = 'SELECT * FROM empleados';

    db.query(sql, (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Error al obtener los datos de empleados' });
        }

        res.json(results);
    });
});

// POST: Agregar empleado
app.post('/empleados', (req, res) => {
    const { nombre, edad, pais, cargo, anios } = req.body;
    
    // Validación de datos
    if (!nombre || !edad || !pais || !cargo || anios === undefined) {
        return res.status(400).json({ error: 'Todos los campos son requeridos' });
    }
    
    if (edad < 0 || anios < 0) {
        return res.status(400).json({ error: 'La edad y años de experiencia deben ser positivos' });
    }
    
    const sql = 'INSERT INTO empleados (nombre, edad, pais, cargo, anios) VALUES (?, ?, ?, ?, ?)';

    db.query(sql, [nombre, edad, pais, cargo, anios], (err, result) => {
        if (err) {
            return res.status(500).json({ error: 'Error al guardar los datos del empleado' });
        }

        // Devolvemos directamente el objeto del empleado con el ID generado
        res.json({
            id: result.insertId,
            nombre,
            edad,
            pais,
            cargo,
            anios
        });
    });
});

// PUT: Actualizar empleado
app.put('/empleados/:id', (req, res) => {
    const { id } = req.params;
    const { nombre, edad, pais, cargo, anios } = req.body;

    // Validación de datos
    if (!nombre || !edad || !pais || !cargo || anios === undefined) {
        return res.status(400).json({ error: 'Todos los campos son requeridos' });
    }
    
    if (edad < 0 || anios < 0) {
        return res.status(400).json({ error: 'La edad y años de experiencia deben ser positivos' });
    }

    const sql = 'UPDATE empleados SET nombre = ?, edad = ?, pais = ?, cargo = ?, anios = ? WHERE id = ?';

    db.query(sql, [nombre, edad, pais, cargo, anios, id], (err, result) => {
        if (err) {
            return res.status(500).json({ error: 'Error al actualizar el empleado' });
        }

        res.json({ message: 'Empleado actualizado correctamente' });
    });
});

// DELETE: Eliminar empleado
app.delete('/empleados/:id', (req, res) => {
    const { id } = req.params;
    const sql = 'DELETE FROM empleados WHERE id = ?';

    db.query(sql, [id], (err, result) => {
        if (err) {
            return res.status(500).json({ error: 'Error al eliminar el empleado' });
        }

        res.json({ message: 'Empleado eliminado correctamente' });
    });
});

app.listen(3001, () => {
    console.log('Servidor del backend corriendo en el puerto 3001');
});
