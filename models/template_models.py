"""
Modelos para el gestor de mensajes utilizando el patrón Builder.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MessageTemplate:
    """Clase que representa una plantilla de mensaje."""
    template: str
    fields: List[str]


@dataclass
class MessageType:
    """Clase que representa un tipo de mensaje dentro de una plataforma."""
    name: str
    templates: Dict[str, MessageTemplate] = field(default_factory=dict)
    
    def add_template(self, template_name: str, template_text: str, fields: List[str]) -> None:
        """Añade una nueva plantilla al tipo de mensaje."""
        self.templates[template_name] = MessageTemplate(template=template_text, fields=fields)
    
    def get_template(self, template_name: str) -> Optional[MessageTemplate]:
        """Obtiene una plantilla por su nombre."""
        return self.templates.get(template_name)


@dataclass
class TemplateBuilder:
    """Builder para construir plantillas de mensajes."""
    platforms: Dict[str, Dict[str, MessageTemplate]] = field(default_factory=dict)
    
    def add_platform(self, platform_name: str) -> None:
        """Añade una nueva plataforma."""
        if platform_name not in self.platforms:
            self.platforms[platform_name] = {}
    
    def add_message_type(self, platform_name: str, message_type: str) -> None:
        """Añade un nuevo tipo de mensaje a una plataforma."""
        if platform_name not in self.platforms:
            self.add_platform(platform_name)
        
        if message_type not in self.platforms[platform_name]:
            self.platforms[platform_name][message_type] = {}
    
    def add_template(self, platform_name: str, message_type: str, 
                    template_text: str, fields: List[str]) -> None:
        """Añade una nueva plantilla a un tipo de mensaje."""
        self.add_message_type(platform_name, message_type)
        self.platforms[platform_name][message_type] = {
            "template": template_text,
            "fields": fields
        }
    
    def get_template(self, platform_name: str, message_type: str) -> Optional[Dict]:
        """Obtiene una plantilla por su plataforma y tipo de mensaje."""
        if platform_name in self.platforms and message_type in self.platforms[platform_name]:
            return self.platforms[platform_name][message_type]
        return None
    
    def get_platforms(self) -> List[str]:
        """Obtiene la lista de plataformas disponibles."""
        return list(self.platforms.keys())
    
    def get_message_types(self, platform_name: str) -> List[str]:
        """Obtiene la lista de tipos de mensaje para una plataforma."""
        if platform_name in self.platforms:
            return list(self.platforms[platform_name].keys())
        return []
    
    def to_dict(self) -> Dict:
        """Convierte el builder a un diccionario para serialización."""
        return self.platforms
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TemplateBuilder':
        """Crea un builder a partir de un diccionario deserializado."""
        builder = cls()
        builder.platforms = data
        return builder
