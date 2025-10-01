#!/usr/bin/env python3
"""
VERSIÓN MINIMALISTA ABSOLUTA PARA VERCEL
Sin ninguna dependencia externa - Solo Gradio básico
"""

import gradio as gr

class MinimalTranslator:
    """Aplicación minimalista que cabe en una sola función."""

    def __init__(self):
        self.languages = {
            'Español': 'es',
            'English': 'en',
            'Français': 'fr',
            'Deutsch': 'de',
            'Italiano': 'it',
            'Português': 'pt'
        }

    def create_interface(self):
        """Crear interfaz ultra-simple."""

        css = """
        .container { max-width: 600px; margin: auto; padding: 10px; }
        .title { text-align: center; color: #333; }
        .panel { background: white; padding: 10px; margin: 10px 0; border-radius: 5px; }
        """

        with gr.Blocks(title="Traductor Minimal", css=css) as interface:
            gr.HTML("<div class='container'><h1 class='title'>🌐 Traductor Minimal</h1></div>")

            with gr.Row():
                with gr.Column():
                    with gr.Group(elem_classes="panel"):
                        gr.HTML("<h3>Entrada</h3>")
                        input_text = gr.Textbox(label="Texto a traducir", lines=3)
                        source_lang = gr.Dropdown(
                            label="Idioma origen",
                            choices=list(self.languages.keys()),
                            value="Español"
                        )

                with gr.Column():
                    with gr.Group(elem_classes="panel"):
                        gr.HTML("<h3>Salida</h3>")
                        output_text = gr.Textbox(label="Texto traducido", lines=3)
                        target_lang = gr.Dropdown(
                            label="Idioma destino",
                            choices=list(self.languages.keys()),
                            value="English"
                        )

            translate_btn = gr.Button("Traducir")

            translate_btn.click(
                fn=self.translate_simple,
                inputs=[input_text, source_lang, target_lang],
                outputs=[output_text]
            )

        return interface

    def translate_simple(self, text, source, target):
        """Traducción ultra-simple."""
        if not text or not text.strip():
            return "Por favor ingresa texto para traducir"

        # Simulación de traducción (en producción usarías APIs reales)
        if source == "Español" and target == "English":
            if "hola" in text.lower():
                return "Hello"
            elif "adiós" in text.lower():
                return "Goodbye"
            else:
                return f"Translated: {text}"
        else:
            return f"Traducción de {source} a {target}: {text}"

    def launch(self, **kwargs):
        interface = self.create_interface()
        interface.launch(**kwargs)

# Función principal
def main():
    app = MinimalTranslator()
    app.launch(share=False)

if __name__ == "__main__":
    main()