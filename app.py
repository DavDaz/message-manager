import flet as ft
from models.template_models import TemplateBuilder
from utils.persistence import TemplateStorage
from utils.template_initializer import initialize_templates

class ConfigScreen:
    def __init__(self, page, on_close_callback):
        self.page = page
        self.on_close_callback = on_close_callback
        self.storage = TemplateStorage()
        self.template_builder = initialize_templates()
        
        # Crear controles
        self.create_ui()
        
    def create_ui(self):
        # Título
        self.title = ft.Text("Configuración del Gestor de Mensajes", size=24, weight=ft.FontWeight.BOLD)
        
        # Botón para volver
        self.back_button = ft.ElevatedButton(
            "Volver al generador",
            on_click=self.close_config
        )
        
        # Tabs para la configuración
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Plataformas",
                    content=self.create_platforms_tab()
                ),
                ft.Tab(
                    text="Tipos de Mensaje",
                    content=self.create_message_types_tab()
                ),
                ft.Tab(
                    text="Plantillas",
                    content=self.create_templates_tab()
                )
            ]
        )
        
        # Contenedor principal
        self.content = ft.Column([
            ft.Row([
                self.title,
                self.back_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            self.tabs
        ], expand=True)
    
    def create_platforms_tab(self):
        # Lista de plataformas
        self.platforms_list = ft.ListView(
            spacing=10,
            padding=20,
            height=300
        )
        
        # Actualizar lista de plataformas
        self.update_platforms_list()
        
        # Campo para nueva plataforma
        self.new_platform_field = ft.TextField(
            label="Nombre de la nueva plataforma",
            width=300
        )
        
        # Botón para agregar plataforma
        add_platform_button = ft.ElevatedButton(
            "Agregar plataforma",
            on_click=self.add_new_platform
        )
        
        return ft.Column([
            ft.Text("Plataformas existentes:", size=16),
            self.platforms_list,
            ft.Divider(),
            ft.Text("Agregar nueva plataforma:", size=16),
            ft.Row([
                self.new_platform_field,
                add_platform_button
            ])
        ], spacing=10)
    
    def update_platforms_list(self):
        self.platforms_list.controls.clear()
        
        for platform in self.template_builder.get_platforms():
            self.platforms_list.controls.append(
                ft.Row([
                    ft.Text(platform, size=16),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Eliminar plataforma",
                        on_click=lambda e, p=platform: self.delete_platform(p)
                    )
                ])
            )
        
        if not self.platforms_list.controls:
            self.platforms_list.controls.append(
                ft.Text("No hay plataformas configuradas", italic=True)
            )
        
        self.page.update()
    
    def add_new_platform(self, e):
        platform_name = self.new_platform_field.value
        
        if not platform_name:
            self.show_snackbar("El nombre de la plataforma no puede estar vacío")
            return
        
        # Agregar plataforma
        self.template_builder.add_platform(platform_name)
        
        # Guardar cambios
        self.storage.save_templates(self.template_builder.to_dict())
        
        # Actualizar lista de plataformas
        self.update_platforms_list()
        
        # Actualizar dropdown de plataformas en la pestaña de tipos de mensaje
        self.update_platform_dropdown()
        
        # Limpiar campo
        self.new_platform_field.value = ""
        
        self.show_snackbar(f"Plataforma '{platform_name}' agregada correctamente")
    
    def delete_platform(self, platform_name):
        # Eliminar plataforma
        if platform_name in self.template_builder.platforms:
            del self.template_builder.platforms[platform_name]
            
            # Guardar cambios
            self.storage.save_templates(self.template_builder.to_dict())
            
            # Actualizar lista de plataformas
            self.update_platforms_list()
            
            # Actualizar dropdown de plataformas en la pestaña de tipos de mensaje
            self.update_platform_dropdown()
            
            self.show_snackbar(f"Plataforma '{platform_name}' eliminada correctamente")
    
    def update_platform_dropdown(self):
        # Actualizar opciones del dropdown de plataformas en la pestaña de tipos de mensaje
        if hasattr(self, 'config_platform_dropdown'):
            self.config_platform_dropdown.options = [
                ft.dropdown.Option(key=platform, text=platform) 
                for platform in self.template_builder.get_platforms()
            ]
        
        # Actualizar opciones del dropdown de plataformas en la pestaña de plantillas
        if hasattr(self, 'template_platform_dropdown'):
            self.template_platform_dropdown.options = [
                ft.dropdown.Option(key=platform, text=platform) 
                for platform in self.template_builder.get_platforms()
            ]
        
        self.page.update()
    
    def create_message_types_tab(self):
        # Dropdown para seleccionar plataforma
        self.config_platform_dropdown = ft.Dropdown(
            label="Selecciona la plataforma",
            width=300,
            options=[ft.dropdown.Option(key=platform, text=platform) 
                    for platform in self.template_builder.get_platforms()],
            on_change=self.update_message_types_list
        )
        
        # Lista de tipos de mensaje
        self.message_types_list = ft.ListView(
            spacing=10,
            padding=20,
            height=300
        )
        
        # Campo para nuevo tipo de mensaje
        self.new_message_type_field = ft.TextField(
            label="Nombre del nuevo tipo de mensaje",
            width=300
        )
        
        # Botón para agregar tipo de mensaje
        add_message_type_button = ft.ElevatedButton(
            "Agregar tipo de mensaje",
            on_click=self.add_new_message_type
        )
        
        return ft.Column([
            ft.Text("Selecciona una plataforma:", size=16),
            self.config_platform_dropdown,
            ft.Divider(),
            ft.Text("Tipos de mensaje existentes:", size=16),
            self.message_types_list,
            ft.Divider(),
            ft.Text("Agregar nuevo tipo de mensaje:", size=16),
            ft.Row([
                self.new_message_type_field,
                add_message_type_button
            ])
        ], spacing=10)
    
    def update_message_types_list(self, e):
        platform = e.control.value
        self.message_types_list.controls.clear()
        
        if platform:
            for message_type in self.template_builder.get_message_types(platform):
                self.message_types_list.controls.append(
                    ft.Row([
                        ft.Text(message_type, size=16),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Eliminar tipo de mensaje",
                            on_click=lambda e, p=platform, mt=message_type: self.delete_message_type(p, mt)
                        )
                    ])
                )
            
            if not self.message_types_list.controls:
                self.message_types_list.controls.append(
                    ft.Text("No hay tipos de mensaje configurados para esta plataforma", italic=True)
                )
        else:
            self.message_types_list.controls.append(
                ft.Text("Selecciona una plataforma para ver sus tipos de mensaje", italic=True)
            )
        
        self.page.update()
    
    def add_new_message_type(self, e):
        platform = self.config_platform_dropdown.value
        message_type = self.new_message_type_field.value
        
        if not platform:
            self.show_snackbar("Debes seleccionar una plataforma")
            return
        
        if not message_type:
            self.show_snackbar("El nombre del tipo de mensaje no puede estar vacío")
            return
        
        # Agregar tipo de mensaje con una plantilla vacía
        self.template_builder.add_template(
            platform_name=platform,
            message_type=message_type,
            template_text="",
            fields=[]
        )
        
        # Guardar cambios
        self.storage.save_templates(self.template_builder.to_dict())
        
        # Actualizar lista de tipos de mensaje
        # Crear un evento con los parámetros requeridos
        self.update_message_types_list(ft.ControlEvent(
            name="change",  # Nombre del evento
            data="",       # Datos adicionales (vacío en este caso)
            page=self.page,  # Referencia a la página
            target=self.config_platform_dropdown,
            control=self.config_platform_dropdown
        ))
        
        # Actualizar dropdown de tipos de mensaje en la pestaña de plantillas
        self.update_message_type_dropdowns(platform)
        
        # Limpiar campo
        self.new_message_type_field.value = ""
        
        self.show_snackbar(f"Tipo de mensaje '{message_type}' agregado correctamente")
    
    def update_message_type_dropdowns(self, platform):
        # Actualizar dropdown de tipos de mensaje en la pestaña de plantillas si está seleccionada la misma plataforma
        if hasattr(self, 'template_platform_dropdown') and self.template_platform_dropdown.value == platform:
            self.template_message_type_dropdown.options.clear()
            self.template_message_type_dropdown.options.extend([
                ft.dropdown.Option(key=msg_type, text=msg_type) 
                for msg_type in self.template_builder.get_message_types(platform)
            ])
            self.page.update()
    
    def delete_message_type(self, platform, message_type):
        # Eliminar tipo de mensaje
        if platform in self.template_builder.platforms and message_type in self.template_builder.platforms[platform]:
            del self.template_builder.platforms[platform][message_type]
            
            # Guardar cambios
            self.storage.save_templates(self.template_builder.to_dict())
            
            # Actualizar lista de tipos de mensaje
            self.update_message_types_list(ft.ControlEvent(
                name="change",
                data="",
                page=self.page,
                target=self.config_platform_dropdown,
                control=self.config_platform_dropdown
            ))
            
            # Actualizar dropdown de tipos de mensaje en la pestaña de plantillas
            self.update_message_type_dropdowns(platform)
            
            self.show_snackbar(f"Tipo de mensaje '{message_type}' eliminado correctamente")
    
    def create_templates_tab(self):
        # Dropdowns para seleccionar plataforma y tipo de mensaje
        self.template_platform_dropdown = ft.Dropdown(
            label="Selecciona la plataforma",
            width=300,
            options=[ft.dropdown.Option(key=platform, text=platform) 
                    for platform in self.template_builder.get_platforms()],
            on_change=self.update_template_message_types
        )
        
        self.template_message_type_dropdown = ft.Dropdown(
            label="Selecciona el tipo de mensaje",
            width=300,
            disabled=True,
            on_change=self.load_template
        )
        
        # Campo para la plantilla
        self.template_text_field = ft.TextField(
            label="Plantilla de mensaje",
            multiline=True,
            min_lines=8,
            max_lines=12,
            width=750
        )
        
        # Contenedor para mostrar los campos detectados (no editable)
        self.template_fields_container = ft.Container(
            content=ft.Column([
                ft.Text("Campos detectados en la plantilla:", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("", size=14, color=ft.Colors.BLUE_700, selectable=True)
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=750
        )
        
        # Texto informativo sobre la detección automática
        self.fields_info_text = ft.Text(
            "Los campos se detectan automáticamente de las variables {variable} en la plantilla",
            size=12,
            italic=True,
            color=ft.Colors.GREY_700
        )
        
        # Botón para guardar plantilla
        save_template_button = ft.ElevatedButton(
            "Guardar plantilla",
            on_click=self.save_template
        )
        
        return ft.Column([
            ft.Text("Selecciona la plataforma y el tipo de mensaje:", size=16),
            ft.Row([
                self.template_platform_dropdown,
                self.template_message_type_dropdown
            ]),
            ft.Divider(),
            ft.Text("Edita la plantilla:", size=16),
            self.template_text_field,
            ft.Text("Campos de la plantilla:", size=16),
            self.template_fields_container,
            self.fields_info_text,
            ft.Container(
                content=save_template_button,
                alignment=ft.alignment.center_right,
                margin=ft.margin.only(top=20)
            )
        ], spacing=10)
    
    def update_template_message_types(self, e):
        platform = e.control.value
        
        # Limpiar y actualizar dropdown de tipos
        self.template_message_type_dropdown.options.clear()
        self.template_message_type_dropdown.options.extend([
            ft.dropdown.Option(key=msg_type, text=msg_type) 
            for msg_type in self.template_builder.get_message_types(platform)
        ])
        self.template_message_type_dropdown.disabled = False
        self.template_message_type_dropdown.value = None
        
        # Limpiar campos
        self.template_text_field.value = ""
        self.template_fields_container.content.controls[1].value = ""
        
        self.page.update()
    
    def load_template(self, e):
        platform = self.template_platform_dropdown.value
        message_type = e.control.value
        
        if platform and message_type:
            template_data = self.template_builder.get_template(platform, message_type)
            
            if template_data:
                self.template_text_field.value = template_data["template"]
                self.template_fields_container.content.controls[1].value = ", ".join(template_data["fields"])
                self.page.update()
    
    def save_template(self, e):
        platform = self.template_platform_dropdown.value
        message_type = self.template_message_type_dropdown.value
        template_text = self.template_text_field.value
        
        if not platform or not message_type:
            self.show_snackbar("Debes seleccionar una plataforma y un tipo de mensaje")
            return
        
        if not template_text.strip():
            self.show_snackbar("La plantilla no puede estar vacía")
            return
        
        # Extraer variables del texto de la plantilla (formato {variable})
        import re
        template_variables = re.findall(r'\{([^\}]+)\}', template_text)
        
        if not template_variables:
            self.show_snackbar("No se detectaron variables en la plantilla. Usa el formato {variable} para definir campos.")
            return
        
        # Actualizar el contenedor de campos con las variables detectadas
        self.template_fields_container.content.controls[1].value = ", ".join(template_variables)
        
        # Guardar plantilla con las variables detectadas
        self.template_builder.add_template(
            platform_name=platform,
            message_type=message_type,
            template_text=template_text,
            fields=template_variables
        )
        
        # Guardar cambios
        self.storage.save_templates(self.template_builder.to_dict())
        
        self.page.update()
        self.show_snackbar("Plantilla guardada correctamente con los campos detectados automáticamente")
    
    def show_snackbar(self, message):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def close_config(self, e):
        self.on_close_callback()

class MessageGeneratorScreen:
    def __init__(self, page, on_config_callback):
        self.page = page
        self.on_config_callback = on_config_callback
        self.storage = TemplateStorage()
        self.template_builder = initialize_templates()
        
        # Variables para almacenar selecciones
        self.selected_platform = None
        self.selected_type = None
        
        # Crear controles
        self.create_ui()
    
    def create_ui(self):
        # Título de la aplicación
        self.title = ft.Text("Gestor de Mensajes", size=30, weight=ft.FontWeight.BOLD)
        
        # Botón de configuración
        self.config_button = ft.ElevatedButton(
            "Configuración",
            on_click=self.open_config
        )
        
        # Dropdown para seleccionar plataforma
        self.platform_dropdown = ft.Dropdown(
            label="Selecciona la plataforma",
            width=400,
            options=[ft.dropdown.Option(key=platform, text=platform) 
                    for platform in self.template_builder.get_platforms()],
            on_change=self.update_message_types
        )
        
        # Dropdown para seleccionar tipo de mensaje
        self.message_type_dropdown = ft.Dropdown(
            label="Selecciona el tipo de mensaje",
            width=400,
            disabled=True,
            on_change=self.generate_fields
        )
        
        # Contenedor para campos dinámicos
        self.fields_container = ft.Column(spacing=10)
        
        # Campo para mostrar el mensaje generado
        self.message_output = ft.TextField(
            label="Mensaje generado",
            multiline=True,
            min_lines=10,
            max_lines=20,
            read_only=True,
            width=750
        )
        
        # Botón para copiar al portapapeles
        self.copy_button = ft.ElevatedButton(
            "Copiar al portapapeles",
            disabled=True,
            on_click=lambda e: self.page.set_clipboard(self.message_output.value)
        )
        
        # Contenedor principal
        self.content = ft.Column([
            ft.Row([
                self.title,
                self.config_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Text("Selecciona la plataforma y el tipo de mensaje:", size=16),
            self.platform_dropdown,
            self.message_type_dropdown,
            ft.Divider(),
            ft.Text("Completa los campos requeridos:", size=16),
            self.fields_container,
            ft.Divider(),
            ft.Row([
                ft.Text("Mensaje generado:", size=16),
                self.copy_button
            ]),
            self.message_output
        ], spacing=10, expand=True)
    
    def update_message_types(self, e):
        self.selected_platform = e.control.value
        
        # Limpiar y actualizar dropdown de tipos
        self.message_type_dropdown.options.clear()
        self.message_type_dropdown.options.extend([
            ft.dropdown.Option(key=msg_type, text=msg_type) 
            for msg_type in self.template_builder.get_message_types(self.selected_platform)
        ])
        self.message_type_dropdown.disabled = False
        self.message_type_dropdown.value = None
        
        # Limpiar campos
        self.fields_container.controls.clear()
        self.message_output.value = ""
        self.copy_button.disabled = True
        
        self.page.update()
    
    def generate_fields(self, e):
        self.selected_type = e.control.value
        
        # Limpiar campos anteriores
        self.fields_container.controls.clear()
        
        if self.selected_platform and self.selected_type:
            # Obtener plantilla
            template_data = self.template_builder.get_template(
                self.selected_platform, self.selected_type
            )
            
            if template_data:
                # Obtener campos requeridos para este tipo de mensaje
                required_fields = template_data["fields"]
                
                # Crear campos de entrada para cada campo requerido
                for field in required_fields:
                    self.fields_container.controls.append(
                        ft.TextField(
                            label=f"Valor para '{field}'",
                            width=400,
                            on_change=lambda _: self.update_preview()
                        )
                    )
                
                # Agregar botón para generar mensaje
                self.fields_container.controls.append(
                    ft.ElevatedButton(
                        "Generar mensaje",
                        on_click=self.generate_message
                    )
                )
        
        self.page.update()
    
    def update_preview(self):
        if self.selected_platform and self.selected_type:
            try:
                # Obtener plantilla
                template_data = self.template_builder.get_template(
                    self.selected_platform, self.selected_type
                )
                
                if template_data:
                    # Recopilar valores de los campos
                    field_values = {}
                    for i, field in enumerate(template_data["fields"]):
                        field_values[field] = self.fields_container.controls[i].value or f"{{{field}}}"
                    
                    # Generar mensaje con los valores actuales
                    template = template_data["template"]
                    preview = template.format(**field_values)
                    
                    # Actualizar campo de salida
                    self.message_output.value = preview
                    self.page.update()
            except Exception as e:
                print(f"Error al actualizar vista previa: {e}")
    
    def generate_message(self, e):
        if self.selected_platform and self.selected_type:
            try:
                # Obtener plantilla
                template_data = self.template_builder.get_template(
                    self.selected_platform, self.selected_type
                )
                
                if template_data:
                    # Recopilar valores de los campos
                    field_values = {}
                    for i, field in enumerate(template_data["fields"]):
                        field_values[field] = self.fields_container.controls[i].value or ""
                    
                    # Generar mensaje con los valores actuales
                    template = template_data["template"]
                    final_message = template.format(**field_values)
                    
                    # Actualizar campo de salida
                    self.message_output.value = final_message
                    self.copy_button.disabled = False
                    
                    # Mostrar notificación
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("Mensaje generado correctamente"),
                        action="OK"
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
            except KeyError as e:
                # Extraer el nombre de la variable que falta (sin comillas)
                missing_field = str(e).strip("'").strip('"')
                
                # Mensaje más claro sobre el error
                error_message = f"Error: Falta el campo '{missing_field}' que aparece como {{{missing_field}}} en la plantilla"
                
                # Sugerencia para resolver el problema
                suggestion = "Edita la plantilla para agregar este campo en la configuración"
                
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Column([
                        ft.Text(error_message),
                        ft.Text(suggestion, size=12, italic=True)
                    ], spacing=5, tight=True),
                    action="OK"
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as e:
                # Mensaje de error más detallado
                error_message = f"Error al generar mensaje: {e}"
                
                # Verificar si es un error de formato
                if "cannot be formatted" in str(e) or "format" in str(e).lower():
                    error_message = "Error en el formato de la plantilla. Verifica que las variables tengan el formato correcto {variable}"
                
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(error_message),
                    action="OK"
                )
                self.page.snack_bar.open = True
                self.page.update()
    
    def open_config(self, e):
        self.on_config_callback()

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Gestor de Mensajes"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = True
    page.scroll = ft.ScrollMode.AUTO
    
    # Función para cambiar entre pantallas
    def switch_to_generator():
        page.controls.clear()
        generator_screen = MessageGeneratorScreen(page, switch_to_config)
        page.add(generator_screen.content)
        page.update()
    
    def switch_to_config():
        page.controls.clear()
        config_screen = ConfigScreen(page, switch_to_generator)
        page.add(config_screen.content)
        page.update()
    
    # Iniciar con la pantalla del generador
    switch_to_generator()

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)
