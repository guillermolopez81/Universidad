# Sistema de Gestión de Empleados

## Configuración Inicial

### 1. Configurar Base de Datos

Antes de ejecutar el proyecto, necesitas crear un archivo `.env` en la carpeta `server/` con la siguiente configuración:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
DB_NAME=empleados_db
PORT=3001
```

### 2. Crear la Base de Datos

Ejecuta el siguiente SQL en tu servidor MySQL:

```sql
CREATE DATABASE empleados_db;
USE empleados_db;

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    pais VARCHAR(50) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    anios INT NOT NULL
);
```

## Instalación y Ejecución

### Servidor (Backend)
```bash
cd server
npm install
npm start
```

### Cliente (Frontend)
```bash
cd client
npm install
npm start
```

## Errores Corregidos

1. ✅ **Archivo .env faltante**: Se agregó documentación para crear el archivo de configuración
2. ✅ **Respuesta incorrecta en POST**: Se corrigió el endpoint para devolver directamente los datos del empleado
3. ✅ **React 19 incompatibilidad**: Se downgradeó a React 18.2.0 para mayor estabilidad
4. ✅ **Manejo de respuestas**: Se unificó el formato de respuesta entre cliente y servidor

## Estructura del Proyecto

```
proyect2/
├── client/          # Frontend React
│   ├── src/
│   │   ├── App.js   # Componente principal
│   │   └── App.css  # Estilos
│   └── package.json
├── server/          # Backend Node.js
│   ├── index.js     # Servidor Express
│   ├── db.js        # Conexión MySQL
│   └── package.json
└── README.md
```

## Funcionalidades

- ✅ Crear empleados
- ✅ Listar empleados
- ✅ Editar empleados
- ✅ Eliminar empleados
- ✅ Interfaz moderna y responsiva


