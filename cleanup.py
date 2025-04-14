import os
import shutil

# Archivos que queremos conservar
files_to_keep = [
    "README.md",
    "app_simple.py",
    "models/template_models.py",
    "utils/persistence.py",
    "utils/template_initializer.py",
    "templates.py",
    "templates_data.json"
]

# Archivos que queremos eliminar
files_to_remove = [
    "app.py",
    "app_builder.py",
    "main.py"
]

def cleanup_project():
    """Limpia el proyecto eliminando archivos innecesarios."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Eliminar archivos específicos
    for file_path in files_to_remove:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"Eliminado: {file_path}")
    
    # Eliminar directorios __pycache__
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_dir = os.path.join(root, dir_name)
                shutil.rmtree(cache_dir)
                print(f"Eliminado: {os.path.relpath(cache_dir, base_dir)}")
    
    # Renombrar app_simple.py a app.py
    app_simple_path = os.path.join(base_dir, "app_simple.py")
    app_path = os.path.join(base_dir, "app.py")
    if os.path.exists(app_simple_path):
        shutil.copy2(app_simple_path, app_path)
        os.remove(app_simple_path)
        print("Renombrado: app_simple.py -> app.py")
    
    print("\nLimpieza completada. El proyecto ahora contiene solo los archivos necesarios.")

if __name__ == "__main__":
    cleanup_project()
