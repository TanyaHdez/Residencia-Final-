# Residencia-Final-
“PLATAFORMA WEB PARA EL ALMACENAMIENTO Y DIAGNÓSTICO MÉDICO DE SEÑALES CARDIOVASCULARES REMOTAS ASISTIDAS POR COMPUTADORA
## Descripción
Esta plataforma web permite el almacenamiento y consulta de señales, además de la clasificación de electrocardiograma (ECG) y fonocardiograma (FCG). Este proyecto forma parte del proyecto de investigación "Proyecto de diagnósgtico asistido por computadora para un sistema de telemedicina de auscultación cardiaca remota" del TecNM Instituto Tecnológico de Tijuana, con número de asignación 20998.24-P como parte de la Residencia Profesional. La plataforma fue diseñada para mejorar el acceso a diagnósticos médicos en zonas de acceso a especialistas limitado.

## Estructura del proyecto
Plataformaweb/
├── backend/
│ ├── server/ # Archivos del backend Node.js con Express
│ ├── public/ # Archivos públicos (frontend)
│ ├── audiocardiaco-clasificador-main/ # Scripts de análisis de audio (Python)
│ ├── package.json # Dependencias y scripts
│ └── node_modules/ # Módulos de Node
├── README.md # Este archivo

## Tecnologías Utilizadas

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Node.js, Express
- **Base de Datos**: MySQL
- **Cloud Storage**: Google Cloud
- **Estilos frontend** –  Bootstrap 4.5.2
- **Procesamiento de señales cardíacas** – Python
  
## Funcionalidades principales.
Registro y gestión de pacientes y doctores
Carga y visualización de fonocardiogramas (.mp3/.wav)
Análisis automático de señales cardíacas (MFCC, energía, eventos S1/S2)
Comentarios clínicos por parte del doctor
Visualización gráfica de los resultados

# Backend/server/main.js
Punto de entrada principal del servidor Express, todas las funcionalidades de todas las páginas .html

# audiocardiaco-clasificador-main/: 
Scripts de análisis de audio cardíaco en Python

# Autenticación y usuarios /login.html
POST /api/login – Iniciar sesión
GET /api/rol – Obtener el rol del usuario (paciente o doctor)
GET /api/usuarios – Listar usuarios registrados
POST /api/registro – Registrar nuevo usuario

# Páginas que pueden visualizar los doctores
Inicio.html
formulario.html
perfil.html
Perfiles-pacientes.html
perfil-del-paciente.html
paciente.html
Datosdepacientes.html

# Páginas que pueden visualizar los pacientes
pacientes-inicio.html
mi-perfil.html
Respuestas-medicos.html

# Páginas que pueden visualizar los administradores
Admin.html
Datosdepacientes.html
Registrodepaciente.html
Perfiles-pacientes.html
