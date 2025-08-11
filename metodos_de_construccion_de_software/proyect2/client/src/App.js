// Importamos useState y useEffect, que son herramientas que nos da React
// useState sirve para guardar datos en memoria. useEffect permite ejecutar funciones cuando se carga la página.
import { useState, useEffect } from 'react';
import './App.css'; // Importamos los estilos de la aplicación

function App() {
  // Estados para guardar lo que el usuario escribe en el formulario
  const [nombre, setNombre] = useState(""); // Guarda el nombre del empleado
  const [edad, setEdad] = useState(0); // Guarda la edad del empleado
  const [pais, setPais] = useState(""); // Guarda el país del empleado
  const [cargo, setCargo] = useState(""); // Guarda el cargo (puesto) del empleado
  const [anios, setAnios] = useState(0); // Guarda los años de experiencia

  // Lista que contiene todos los empleados registrados
  const [registros, setRegistros] = useState([]); // Arreglo con los empleados obtenidos del backend

  // Este estado se usa para saber si estamos editando un empleado ya existente
  // Si es null, es un nuevo registro. Si tiene un valor, es el índice del empleado a editar.
  const [editIndex, setEditIndex] = useState(null); // Índice del registro que se está editando

  // Cuando se carga la página, obtenemos los empleados desde el backend (Node.js y MySQL)
  useEffect(() => {
    // Definimos una función asíncrona interna para cargar empleados
    const cargarEmpleados = async () => {
      try {
        const response = await fetch('http://localhost:3001/empleados'); // Hacemos la petición GET al backend
        if (response.ok) {
          const data = await response.json(); // Parseamos la respuesta a JSON
          setRegistros(data); // Guardamos los empleados en el estado "registros"
        } else {
          console.error('Error al cargar empleados:', response.status);
          alert('Error al cargar los empleados. Verifica que el servidor esté funcionando.');
        }
      } catch (error) {
        console.error('Error de conexión:', error);
        alert('Error de conexión. Verifica que el servidor esté funcionando en http://localhost:3001');
      }
    };

    cargarEmpleados(); // Ejecutamos la función al montar el componente
  }, []); // Arreglo de dependencias vacío: se ejecuta solo una vez al inicio

  // Esta función se ejecuta al presionar el botón "Registrar" o "Actualizar"
  const registrarDatos = async (e) => {
    e.preventDefault(); // Evitamos que se recargue la página al enviar el formulario

    // Validación básica en el cliente
    if (!nombre.trim() || !pais.trim() || !cargo.trim() || edad <= 0 || anios < 0) {
      alert('Por favor completa todos los campos correctamente');
      return;
    }

    if (editIndex !== null) {
      // Si estamos editando un empleado existente
      try {
        const empleado = registros[editIndex]; // Obtenemos el empleado actual por índice

        // Enviamos la petición PUT al backend para actualizar ese empleado
        const response = await fetch(`http://localhost:3001/empleados/${empleado.id}`, {
          method: 'PUT', // Método HTTP para actualizar
          headers: { 'Content-Type': 'application/json' }, // Indicamos que enviamos JSON
          body: JSON.stringify({ nombre, edad, pais, cargo, anios }) // Datos actualizados
        });

        if (response.ok) {
          const nuevosRegistros = [...registros]; // Copiamos el array actual de registros
          // Reemplazamos el objeto en la posición editada con los nuevos valores
          nuevosRegistros[editIndex] = { ...empleado, nombre, edad, pais, cargo, anios };
          setRegistros(nuevosRegistros); // Actualizamos el estado con la lista modificada
          setEditIndex(null); // Salimos del modo edición
          alert('Empleado actualizado correctamente'); // Informamos éxito
        } else {
          const errorData = await response.json();
          alert(`Error al actualizar: ${errorData.error || 'Error desconocido'}`);
        }
      } catch (error) {
        alert('Error de conexión al actualizar'); // Error de red o servidor caído
      }
    } else {
      // Si es un nuevo empleado (no estamos editando)
      try {
        const response = await fetch('http://localhost:3001/empleados', {
          method: 'POST', // Método HTTP para crear
          headers: { 'Content-Type': 'application/json' }, // Enviamos JSON
          body: JSON.stringify({ nombre, edad, pais, cargo, anios }) // Datos del nuevo empleado
        });
        
        if (response.ok) {
          const data = await response.json(); // Parseamos la respuesta
          setRegistros([...registros, data]); // Agregamos el nuevo empleado a la lista existente
          alert('Empleado guardado correctamente'); // Informamos éxito
        } else {
          const errorData = await response.json();
          alert(`Error al guardar: ${errorData.error || 'Error desconocido'}`);
        }
      } catch (error) {
        alert('Error de conexión'); // Error de red o servidor caído
      }
    }

    // Limpiamos los campos del formulario (dejamos el formulario listo para un nuevo registro)
    setNombre(""); // Limpia el nombre
    setEdad(0); // Reinicia la edad a 0
    setPais(""); // Limpia el país
    setCargo(""); // Limpia el cargo
    setAnios(0); // Reinicia años de experiencia a 0
  };

  // Esta función se ejecuta cuando el usuario hace clic en "Eliminar"
  const eliminarRegistro = async (idx) => {
    const empleado = registros[idx]; // Obtenemos el empleado a eliminar por el índice
    try {
      const response = await fetch(`http://localhost:3001/empleados/${empleado.id}`, {
        method: 'DELETE' // Método HTTP para eliminar
      });

      if (response.ok) {
        // Si el backend eliminó correctamente, actualizamos el estado filtrando el índice
        setRegistros(registros.filter((_, i) => i !== idx)); // Quitamos el elemento con ese índice
        if (editIndex === idx) {
          // Si estábamos editando justo ese registro, limpiamos el formulario y el modo edición
          setEditIndex(null);
          setNombre("");
          setEdad(0);
          setPais("");
          setCargo("");
          setAnios(0);
        }
        alert('Empleado eliminado correctamente'); // Mensaje de éxito
      } else {
        alert('Error al eliminar el empleado'); // Error de API (no 2xx)
      }
    } catch (error) {
      alert('Error de conexión al eliminar'); // Error de red o servidor caído
    }
  };

  // Esta función se ejecuta cuando se quiere editar un registro ya guardado
  const editarRegistro = (idx) => {
    const reg = registros[idx]; // Obtenemos el empleado por el índice
    setNombre(reg.nombre); // Cargamos el nombre en el formulario
    setEdad(reg.edad); // Cargamos la edad en el formulario
    setPais(reg.pais); // Cargamos el país en el formulario
    setCargo(reg.cargo); // Cargamos el cargo en el formulario
    setAnios(reg.anios); // Cargamos los años de experiencia en el formulario
    setEditIndex(idx); // Marcamos que estamos editando ese empleado (guardamos el índice)
  };

  // Aquí empieza la parte visual que ve el usuario
  return (
    <div className="App">{/* Contenedor principal de la aplicación */}
      {/* Formulario para ingresar los datos */}
      <div className="datos">{/* Contenedor del formulario */}
        <label> Nombre:{/* Etiqueta del input de nombre */}
          <input
            type="text" /* Campo de texto */
            value={nombre} /* Valor controlado por el estado 'nombre' */
            onChange={(e) => setNombre(e.target.value)} /* Actualiza 'nombre' al escribir */
          />
        </label>
        <label> Edad:{/* Etiqueta del input de edad */}
          <input
            type="number" /* Campo numérico */
            value={edad} /* Valor controlado por 'edad' */
            onChange={(e) => setEdad(Number(e.target.value))} /* Convierte a número y guarda */
          />
        </label>
        <label> País:{/* Etiqueta del input de país */}
          <input
            type="text" /* Campo de texto */
            value={pais} /* Valor controlado por 'pais' */
            onChange={(e) => setPais(e.target.value)} /* Actualiza 'pais' */
          />
        </label>
        <label> Cargo:{/* Etiqueta del input de cargo */}
          <input
            type="text" /* Campo de texto */
            value={cargo} /* Valor controlado por 'cargo' */
            onChange={(e) => setCargo(e.target.value)} /* Actualiza 'cargo' */
          />
        </label>
        <label> Años:{/* Etiqueta del input de años de experiencia */}
          <input
            type="number" /* Campo numérico */
            value={anios} /* Valor controlado por 'anios' */
            onChange={(e) => setAnios(Number(e.target.value))} /* Convierte a número y guarda */
          />
        </label>

        {/* Botón que cambia de texto dependiendo si es nuevo o edición */}
        <button onClick={registrarDatos}>
          {editIndex !== null ? 'Actualizar' : 'Registrar'}{/* Texto dinámico del botón */}
        </button>
      </div>

      {/* Tabla con los empleados registrados */}
      {registros.length > 0 && ( /* Solo mostramos la tabla si hay registros */
        <div className="tabla-container">{/* Contenedor para estilos de la tabla */}
          <table className="tabla-registros">{/* Tabla de empleados */}
            <thead>{/* Cabecera de la tabla */}
              <tr>{/* Fila de encabezados */}
                <th>Nombre</th>{/* Columna: Nombre */}
                <th>Edad</th>{/* Columna: Edad */}
                <th>País</th>{/* Columna: País */}
                <th>Cargo</th>{/* Columna: Cargo */}
                <th>Años</th>{/* Columna: Años de experiencia */}
                <th>Acciones</th>{/* Columna: Botones de acción */}
              </tr>
            </thead>
            <tbody>{/* Cuerpo de la tabla */}
              {registros.map((reg, idx) => ( /* Recorremos cada registro con su índice */
                <tr key={idx}>{/* Fila por empleado (key = índice) */}
                  <td>{reg.nombre}</td>{/* Celda: nombre del empleado */}
                  <td>{reg.edad}</td>{/* Celda: edad del empleado */}
                  <td>{reg.pais}</td>{/* Celda: país del empleado */}
                  <td>{reg.cargo}</td>{/* Celda: cargo del empleado */}
                  <td>{reg.anios}</td>{/* Celda: años de experiencia */}
                  <td>{/* Celda: acciones */}
                    <button
                      className="btn-editar" /* Clase CSS para estilos */
                      onClick={() => editarRegistro(idx)} /* Al hacer clic, cargamos los datos en el formulario */
                    >
                      Editar
                    </button>
                    <button
                      className="btn-eliminar" /* Clase CSS para estilos */
                      onClick={() => eliminarRegistro(idx)} /* Al hacer clic, eliminamos el registro */
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App; // Exportamos el componente para poder usarlo en otros archivos
