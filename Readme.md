# Aulas_Scrum - Sistema de Gestión de Reservas

Este proyecto es una solución integral diseñada para la administración y control de espacios académicos, permitiendo a los usuarios gestionar el ciclo de vida completo de las reservas de aulas de manera eficiente y segura a través de una interfaz gráfica moderna.

## 📌 Propósito del Proyecto
El objetivo principal de **Aulas_Scrum** es optimizar la asignación de espacios físicos dentro de una institución educativa. El sistema resuelve la problemática de los conflictos de horarios y la falta de visibilidad de la disponibilidad, proporcionando una herramienta intuitiva para realizar las operaciones fundamentales de gestión (CRUD): Registro, Consulta, Modificación y Cancelación de apartados.

## 🛠️ Tecnologías Utilizadas
El software ha sido desarrollado bajo un stack tecnológico enfocado en la ligereza, la estabilidad y la portabilidad:

* **Lenguaje:** Python 3.10+
* **Interfaz Gráfica:** Tkinter (GUI) con diseño personalizado y manejo de estados dinámicos.
* **Base de Datos:** SQLite 3 (Motor relacional integrado para persistencia de datos en `reservas.db`).
* **Control de Versiones:** Git & GitHub (Flujo de trabajo basado en ramas de características como `feature/cancelar`).
* **Editor de Desarrollo:** Visual Studio Code (Configurado como editor principal del sistema).

### 👥 Información del Equipo (Team SoftwarePlus)

El desarrollo del proyecto se rige bajo la metodología **Scrum**, con la siguiente distribución de roles y responsabilidades clave:

| Nombre | Rol Principal | Responsabilidades Key |
| :--- | :--- | :--- |
| **Fabian Camilo Aguilera Rodriguez** | Product Owner (PO) | Definición de requerimientos y priorización del backlog. |
| **Samuel Albeiro Lesmes Hernandez** | Scrum Master (SM) / Dev | Facilitador de procesos y desarrollo de lógica central. |
| **Nicolle Camila Piñeros Castañeda** | Desarrollador 1 | Diseño de interfaces (UI) y experiencia de usuario. |
| **Juan Santiago Lagos Jaimes** | Desarrollador 2 | Gestión de bases de datos SQL y módulos de persistencia. |

## 📂 Estructura Principal del Repositorio
### La arquitectura del proyecto está organizada de forma modular para facilitar el mantenimiento:
 
### 📂 Estructura del Proyecto

#### El repositorio está organizado de manera modular para facilitar el mantenimiento y la escalabilidad del sistema:

```text
Aulas_Scrum/
├── menu_principal.py      # Punto de entrada de la aplicación y menú interactivo.
├── consultas.py           # Módulo de visualización y búsqueda de reservas existentes.
├── registroReservas.py    # Lógica y formularios para la creación de nuevos registros.
├── cancelar.py            # Módulo de eliminación con sistema de confirmación de datos.
├── reservas.db            # Base de datos relacional (SQLite) para persistencia.
└── README.md              # Documentación completa del proyecto y del equipo.
```

## 🚀 Instrucciones de Instalación y Ejecución

### Requisitos Previos
1. Tener instalado **Python 3.x** en su sistema.
2. Contar con un cliente **Git** configurado.

### Instalación
## Clone el repositorio en su máquina local:
### https://github.com/samuellesmes45ex/Aulas_Scrum.git

### Enlace del drive donde se encuentra el video: https://drive.google.com/file/d/1uwNjh8f5kGdtcowSxe-AZsggPGkeLhmZ/view?usp=sharing
### Documento del trabajo Scrum realizado por el grupo: https://drive.google.com/file/d/1W0BkHAoQ4IluB1rkFLOcrKR_82LI3blK/view?usp=sharing
### Documento de la presentación Scrum del grupo: https://www.canva.com/design/DAHEUK-8jOw/uNpk4c9jay8ATEKP0sDdSg/edit?utm_content=DAHEUK-8jOw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
### 