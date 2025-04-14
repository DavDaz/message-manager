"""
Inicializador de plantillas predeterminadas para el gestor de mensajes.
"""
from models.template_models import TemplateBuilder
from utils.persistence import TemplateStorage
from templates import templates as default_templates


def initialize_templates() -> TemplateBuilder:
    """
    Inicializa el builder de plantillas con las plantillas predeterminadas
    o las cargadas desde el archivo de persistencia.
    
    Returns:
        TemplateBuilder: Builder con las plantillas inicializadas.
    """
    # Intentar cargar plantillas guardadas
    storage = TemplateStorage()
    saved_templates = storage.load_templates()
    
    if saved_templates:
        # Si hay plantillas guardadas, usarlas
        return TemplateBuilder.from_dict(saved_templates)
    else:
        # Si no hay plantillas guardadas, usar las predeterminadas
        builder = TemplateBuilder()
        
        # Convertir las plantillas predeterminadas al nuevo formato
        for platform, message_types in default_templates.items():
            builder.add_platform(platform)
            
            for message_type, template_data in message_types.items():
                builder.add_template(
                    platform_name=platform,
                    message_type=message_type,
                    template_text=template_data["template"],
                    fields=template_data["fields"]
                )
        
        # Guardar las plantillas predeterminadas
        storage.save_templates(builder.to_dict())
        
        return builder
