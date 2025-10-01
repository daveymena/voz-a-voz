#!/usr/bin/env python3
"""
API mínima para Vercel - Sin launch, solo funciones directas
"""

import gradio as gr
import json

def create_app():
    """Crear la aplicación Gradio."""

    css = """
    body { font-family: Arial, sans-serif; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    """

    with gr.Blocks(css=css) as app:
        gr.HTML("<h1 style='text-align: center;'>🌐 Traductor Simple</h1>")

        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(label="Texto a traducir")
                source_lang = gr.Dropdown(
                    label="Idioma origen",
                    choices=["Español", "English", "Français"],
                    value="Español"
                )

            with gr.Column():
                output_text = gr.Textbox(label="Texto traducido")
                target_lang = gr.Dropdown(
                    label="Idioma destino",
                    choices=["Español", "English", "Français"],
                    value="English"
                )

        btn = gr.Button("Traducir")

        def translate(text, source, target):
            if not text:
                return "Por favor ingresa texto"

            # Traducción simple
            if source == "Español" and target == "English":
                return "Hello" if "hola" in text.lower() else f"Translated: {text}"
            else:
                return f"Traducción: {text}"

        btn.click(translate, inputs=[input_text, source_lang, target_lang], outputs=[output_text])

    return app

# Para Vercel - función principal que retorna la app
app = create_app()