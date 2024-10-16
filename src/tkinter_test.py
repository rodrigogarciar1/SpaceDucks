import tkinter as tk

# Función que se ejecuta al presionar el botón
def mostrar_texto():
    texto_ingresado = entry.get()  # Obtiene el texto del cuadro de texto
    label_resultado.config(text=texto_ingresado)  # Muestra el texto debajo del botón

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ventana con Texto Personalizable")

# Crear el cuadro de texto
entry = tk.Entry(ventana, font=("Arial", 14), width=30)
entry.pack(pady=10)

# Crear el botón
boton = tk.Button(ventana, text="Mostrar Texto", font=("Arial", 14), command=mostrar_texto)
boton.pack(pady=10)

# Crear la etiqueta para mostrar el texto ingresado
label_resultado = tk.Label(ventana, text="", font=("Arial", 14))
label_resultado.pack(pady=10)

# Iniciar el bucle principal de la ventana
ventana.mainloop()