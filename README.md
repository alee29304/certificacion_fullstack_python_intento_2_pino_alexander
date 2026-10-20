# Querido Diario 📖

## Descripción del Proyecto
**Querido Diario** Desarrollé una aplicación web en Python utilizando el marco Flask y MySQL como base de datos. La idea del proyecto es permitir que los usuarios puedan crear, ver, editar, buscar y eliminar notas o entradas con fechas e información relevante de manera sencilla.   El funcionamiento del sistema se divide en varias partes clave:Por un lado está la gestión de usuarios, que permite registrarse e iniciar sesión de forma privada para que cada persona controle solo sus propias publicaciones. Luego está la lógica propia de las entradas, que se encarga de procesar los formularios para guardar notas nuevas, mostrarlas en detalle, actualizarlas o buscarlas dentro del sitio.

## Funciones Principales Utilizadas en el Proyecto

### A nivel interno, la app consulta la base de datos MySQL para leer y guardar la información de los usuarios y de las notas. Toda la parte visual está construida con archivos HTML que representan las distintas pantallas (como el inicio, la vista de login, el formulario para crear o editar notas y el buscador) acompañados por un archivo de estilos CSS para el diseño.   Finalmente, el proyecto cuenta con un archivo principal que se encarga de arrancar el servidor web, junto con archivos de configuración para manejar variables de entorno y las librerías instaladas en Python. 

## Estructura de Archivos del Proyecto
certificacion_fullstack_python/
│
├── flask_app/
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├── entradas_controllers.py
│   │   └── usuarios_controllers.py
│   │
│   ├── models/
│   │   ├── entrada.py
│   │   └── Usuario.py
│   │
│   ├── resources/
│   │   └── db/
│   │       ├── esquema_entradas.sql
│   │       └── erd_entradas.png
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   │   ├── 404.html
│   │   ├── base.html
│   │   ├── buscar.html
│   │   ├── editar_entrada.html
│   │   ├── inicio.html
│   │   ├── login.html
│   │   ├── nueva_entrada.html
│   │   └── ver_entrada.html
│   │
│   └── __init__.py
│
├── .env
├── .env.example
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── README.md
├── requirements.txt
└── server.py

AUTOR:
Alexander Pino