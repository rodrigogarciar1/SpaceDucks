import dearpygui.dearpygui as dpg  # Importamos la librería Dear PyGui

dpg.create_context()  # Inicializa el entorno de Dear PyGui

opcion = int(input("Selecciona una opción: \n1. Mensaje de Bienvenida \n2. Botón con mensaje \n3. Botones con callback \n4. Sliders \n5. Gráfico \n6. Tabla\n"))
# Opción 1: Ventana con mensaje de bienvenida
if opcion == 1:
    with dpg.window(label="Ventana Principal", width=400, height=300):
        dpg.add_text("¡Bienvenido a Dear PyGui!")
        dpg.add_button(label="Botón")

# Opción 2: Ventana con botón que actualiza un mensaje en la propia ventana
elif opcion == 2:
    with dpg.window(label="Ventana Principal", width=400, height=300):
        text_widget = dpg.add_text("Presiona el botón para ver un mensaje aquí.")  # Crea un widget de texto vacío

        # Función que actualiza el texto cuando se presiona el botón
        def actualizar_texto(sender, app_data, user_data):
            dpg.set_value(text_widget, "¡Botón presionado!")  # Cambia el texto cuando el botón es presionado

        dpg.add_button(label="Presióname", callback=actualizar_texto)

# Opción 3: Ventana con dos botones que imprimen mensajes en la consola
elif opcion == 3:
    with dpg.window(label="Ventana con Botones", width=600, height=600):  
        dpg.add_button(label="Botón 1", callback=lambda: print("Botón 1 presionado")) 
        dpg.add_button(label="Botón 2", callback=lambda: print("Botón 2 presionado")) 

# Opción 4: Ventana con un control deslizante (slider)
elif opcion == 4:
    with dpg.window(label="Ventana con Sliders"):
        dpg.add_slider_float(label="Control Deslizante", default_value=0.5, max_value=1.0)  # Agrega un slider

# Opción 5: Ventana con un gráfico simple
elif opcion == 5:
    with dpg.window(label="Gráfico de Ejemplo"): 
        with dpg.plot(label="Gráfico de Datos", height=300, width=400):  # Crea un área para un gráfico
            dpg.add_plot_legend()  # Agrega una leyenda al gráfico
            dpg.add_plot_axis(dpg.mvXAxis, label="Eje X")  # Agrega el eje X
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Eje Y")  # Agrega el eje Y
            # Agrega una serie de datos (línea) al gráfico
            dpg.add_line_series([0, 1, 2, 3, 4], [10, 12, 8, 10, 14], parent=y_axis, label="Datos")

# Opción 6: Ventana con una tabla simple
elif opcion == 6:
    with dpg.window(label="Tabla de Ejemplo", width=400, height=300):  # Crea una ventana
        with dpg.table(header_row=True):  # Crea una tabla con fila de encabezado
            dpg.add_table_column(label="Columna 1")  
            dpg.add_table_column(label="Columna 2")  
            dpg.add_table_column(label="Columna 3")  

            # Agrega una fila con tres celdas de datos
            with dpg.table_row():
                dpg.add_text("Dato 1")
                dpg.add_text("Dato 2")
                dpg.add_text("Dato 3")

            # Agrega otra fila con tres celdas de datos
            with dpg.table_row():
                dpg.add_text("Dato 4")
                dpg.add_text("Dato 5")
                dpg.add_text("Dato 6")

# Si el usuario ingresa una opción inválida
else:
    print("Opción no válida. Por favor, selecciona un número entre 1 y 6.")

# Configuración y despliegue de la ventana principal
dpg.create_viewport(title='Aplicación con Dear PyGui', width=600, height=400)  # Crea y configura la ventana principal
dpg.setup_dearpygui()  # Configura el entorno de Dear PyGui
dpg.show_viewport()  # Muestra la ventana
dpg.start_dearpygui()  # Inicia el ciclo de Dear PyGui (se mantiene la ventana abierta)
dpg.destroy_context()  # Libera los recursos al cerrar la ventana


