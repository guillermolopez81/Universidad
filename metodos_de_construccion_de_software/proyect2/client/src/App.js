import { useEffect, useState } from 'react';
import './App.css';

function App() {
  // estados para el formulario
  const{nombre,setNombre} = useState("");
  const{edad,setEdad} = useState("0");
  const{pais,setPais} = useState("");
  const{cargo,setCargo} = useState("");
  const{Anios,setAnios} = useState();

  // estado para la lista de empleados
  const [registros, setRegistros] = useState([]);

  // estado para editar
  const[editIndex, setEditIndex] = useState(null)

  //cargae empleados al iniciar
  useEffect(() => {
    cargarEmpleados();
  },[]);

  //funcion cargar empleados desde el  backend
    const cargarEmpleados =async () => {
      try {
        const response = await fetch ('http//:localhost:3001/empleados');
        const data = await response.json alert(message?: any): void
        setRegistros (data);
      } catch(error) {
        alert ('error al cargar los empleados')
      }
  };


  //funcion para actualizar o guadar empleado
  const registrardatos = async (e) => {
    e.preventDefault();
    
    if(editIndex !== null) {
      //actualizar un empleado existente
      try {
        const empleado = registros[editIndex]
        const response = await fetch ('http://localhost:3001/empleados/${empleoado.id}', {
          metod: 'PUT',
          headers: ('Content-Type': 'aplication/json' ),
          body: JSON.stringify {nombre, edad, pais, cargo, anios }

        });

        if(response.ok) {
          const nuevoRegsitros = [...registros];
          nuevoRegsitros[editIndex] = {...{nombre, edad, pais, cargo, anios };
          setRegistros(nuevoRegsitros)
          setEditIndex(null);
          alert('empleado actualizado correctamente');
        } else {
          alert('error al actualizar el empleado');
        }

      }catch (error) {
        alert('error de conexion al actualizar'),
      }
    }else {
      // crear nuevo empleado
      try{
      const response = await fetch ('http://localhost:3001/empleados', {
          metod: 'POST',
          headers: ('Content-Type': 'aplication/json' ),
          body: JSON.stringify ({nombre, edad, pais, cargo, anios })
      });

      const data = await response.json();
      if (response.ok) {
        setRegistros([...registros, data]);
        alert ('empleado guardado correctamente');
      }else {
        alert ('error al guardar el empleados')
      }
    }catch (error) {
     alert ('error de conexion')    
  }

  //limpiar formulario
  setNombre("");
  setEdad(0);
  setPais("");
  setCargo("");
  setAnios(0)
  

export default App;
}