"""
Archivo que contiene los templates para la generación de mensajes.
"""

templates = {
    "Tickets": {
        "Anulación": {
            "template": """\
Asunto: Anulación de entrada

Hola {remitente},

Se anuló la entrada {numero_entrada} correspondiente a {nombre_persona}, cédula {cedula}.

Cualquier otro detalle que necesites, me avisas.

Saludos,
{firma}
""",
            "fields": ["remitente", "numero_entrada", "nombre_persona", "cedula", "firma"]
        },
        "Actualización": {
            "template": """\
Asunto: Actualización de entrada

Hola {remitente},

Se actualizó la información de la entrada {numero_entrada} vinculada a {nombre_persona}, cédula {cedula}. Los cambios fueron registrados correctamente.

Saludos,
{firma}
""",
            "fields": ["remitente", "numero_entrada", "nombre_persona", "cedula", "firma"]
        }
    },
    "Correos": {
        "Seguimiento": {
            "template": """\
Asunto: Seguimiento a solicitud

Hola {nombre},

Solo para dar seguimiento a la solicitud con referencia {referencia}. Quedamos atentos a cualquier actualización de tu parte.

Saludos,
{firma}
""",
            "fields": ["nombre", "referencia", "firma"]
        }
    }
}
