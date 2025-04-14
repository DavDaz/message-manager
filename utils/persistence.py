"""
Utilidades para la persistencia de datos en el gestor de mensajes.
"""
import json
import os
from typing import Dict, Any


class TemplateStorage:
    """Clase para gestionar la persistencia de las plantillas."""
    
    def __init__(self, file_path: str = "templates_data.json"):
        """
        Inicializa el almacenamiento de plantillas.
        
        Args:
            file_path: Ruta del archivo donde se guardarán las plantillas.
        """
        self.file_path = file_path
    
    def save_templates(self, templates_data: Dict[str, Any]) -> bool:
        """
        Guarda los datos de las plantillas en un archivo JSON.
        
        Args:
            templates_data: Datos de las plantillas a guardar.
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(templates_data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar las plantillas: {e}")
            return False
    
    def load_templates(self) -> Dict[str, Any]:
        """
        Carga los datos de las plantillas desde un archivo JSON.
        
        Returns:
            Dict: Datos de las plantillas cargados o un diccionario vacío si no existe el archivo.
        """
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar las plantillas: {e}")
            return {}
