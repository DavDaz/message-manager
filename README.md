# Gestor de Mensajes

Una aplicación para generar mensajes a partir de plantillas predefinidas, con una interfaz gráfica moderna y capacidad de configuración dinámica.

## Características

- Interfaz gráfica moderna con Flet
- Patrón Builder para la creación de mensajes
- Persistencia de datos para guardar configuraciones
- Capacidad para agregar, editar y eliminar:
  - Plataformas
  - Tipos de mensajes
  - Plantillas
- Vista previa en tiempo real
- Copiado al portapapeles

## Estructura del Proyecto

```
gestor-mensajes/
├── app.py                # Aplicación principal con interfaz gráfica
├── templates.py          # Plantillas predeterminadas
├── templates_data.json   # Archivo de persistencia de datos
├── models/
│   └── template_models.py  # Modelos para el patrón Builder
└── utils/
    ├── persistence.py      # Utilidades para la persistencia de datos
    └── template_initializer.py  # Inicializador de plantillas
```

## Requisitos

- Python 3.6+
- Flet

## Instalación rápida

Para instalar las dependencias necesarias:

```bash
pip install flet
```

## Cómo usar

1. Instala las dependencias y ejecuta la aplicación:

```console
~$ pip install flet
~$ python app.py
```

O usando Flet directamente:

```console
~$ pip install flet
~$ flet run app.py
```

## Ejecutar con entorno virtual

1. Crear el entorno virtual:
   ```console
   $ python -m venv venv
   ```

2. Activar el entorno virtual:
   - En Windows:
   ```console
   $ venv\Scripts\activate
   ```
   - En macOS/Linux:
   ```console
   $ source venv/bin/activate
   ```

3. Instalar las dependencias:
   ```console
   $ pip install flet
   ```

4. Ejecutar la aplicación:
   ```console
   $ python app.py
   ```
   O usando Flet:
   ```console
   $ flet run app.py
   ```

## Crear ejecutable

Para crear un archivo ejecutable de la aplicación:

```console
~$ flet pack app.py
```

Con un icono personalizado:

```console
~$ flet pack app.py --icon icon.png
```

## Patrón Builder

La aplicación utiliza el patrón Builder para la creación de mensajes, lo que permite:

1. Separar la construcción de objetos complejos de su representación
2. Crear diferentes representaciones del mismo objeto
3. Construir objetos paso a paso
4. Ocultar detalles de implementación

## Persistencia de Datos

Los datos de configuración se guardan en un archivo JSON (`templates_data.json`) que se crea automáticamente. Esto permite:

1. Guardar las configuraciones entre sesiones
2. Compartir configuraciones entre diferentes instancias de la aplicación
3. Editar las configuraciones manualmente si es necesario

## Configuración

La aplicación permite configurar:

1. **Plataformas**: Categorías principales para organizar los mensajes (ej. Tickets, Correos)
2. **Tipos de Mensaje**: Subcategorías dentro de cada plataforma (ej. Anulación, Actualización)
3. **Plantillas**: El texto del mensaje con marcadores de posición para los campos variables
4. **Campos**: Los valores que se pueden personalizar en cada mensaje

## Desarrollador

- [David Diaz]

## Licencia

Este proyecto está bajo la Licencia MIT.
