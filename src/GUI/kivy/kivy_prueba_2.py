from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class SimpleApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')  #se puede poner horizontal o vertical

        # Creamos un TextInput (campo de texto)
        self.text_input = TextInput(hint_text="Escribe aquí", font_size=24, size_hint=(1, 0.2))
        layout.add_widget(self.text_input)

        # Creamos un botón
        button = Button(text="Presionar", font_size=24, size_hint=(1, 0.5)) 
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)

        return layout

    # Función que se llama cuando el botón es presionado
    def on_button_press(self,instance):
        texto_ingresado = self.text_input.text
        print(f"Texto ingresado: {texto_ingresado}")

if __name__ == '__main__':
    SimpleApp().run()
